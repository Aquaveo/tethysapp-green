import logging
from gsshapyorm.orm import ProjectFile, LinkNodeDatasetFile, IndexMap, RasterMapFile
from tethys_gizmos.gizmo_options import MapView
from tethysext.atcore.services.map_manager import MapManagerBase
from tethysapp.green.services.helpers import compute_raster_stats
from tethysapp.green.app import Green as app


log = logging.getLogger(__name__)


class GreenMapManager(MapManagerBase):
    """
    Object that orchestrates the map layers and resources for Green app.
    """
    MAP_VIEW_VERSION = '4.6.5'
    MAX_ZOOM = 28
    MIN_ZOOM = 4
    DEFAULT_ZOOM = 13

    LND_DISPLAY_NAMES = {
        'cdp': 'Channel Depth',
        'cdq': 'Channel Discharge',
        'cst': 'Channel Stage',
        'cvl': 'Channel Velocity',
    }

    def get_map_preview_url(self):
        """
        Get url for map preview image.

        Returns:
            str: preview image url.
        """
        # Get model boundary name and style
        model_boundary_layer = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_MODEL_BOUNDARY,
            model_db=self.model_db
        )

        model_boundary_style = self.spatial_manager.get_unique_item_name(self.spatial_manager.VL_MODEL_BOUNDARY)

        # Get stream name and style
        stream_layer = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_STREAM_LINKS,
            model_db=self.model_db
        )
        stream_style = self.spatial_manager.get_unique_item_name(self.spatial_manager.VL_STREAM_LINKS)

        # Default image url
        layer_preview_url = None

        try:
            extent = self.map_extent

            # Calculate preview layer height and width ratios
            if extent:
                # Calculate image dimensions
                long_dif = abs(extent[0] - extent[2])
                lat_dif = abs(extent[1] - extent[3])
                hw_ratio = float(long_dif) / float(lat_dif)
                max_dim = 300

                if hw_ratio < 1:
                    width_resolution = int(hw_ratio * max_dim)
                    height_resolution = max_dim
                else:
                    height_resolution = int(max_dim / hw_ratio)
                    width_resolution = max_dim

                wms_endpoint = self.spatial_manager.get_wms_endpoint()

                layer_preview_url = ('{}?'
                                     'service=WMS&'
                                     'version=1.1.0&'
                                     'request=GetMap&'
                                     'layers={},{}&'
                                     'styles={},{}&'
                                     'bbox={},{},{},{}&'
                                     'width={}&'
                                     'height={}&'
                                     'srs=EPSG:4326&'
                                     'format=image%2Fpng').format(wms_endpoint,
                                                                  model_boundary_layer, stream_layer,
                                                                  model_boundary_style, stream_style,
                                                                  extent[0], extent[1], extent[2], extent[3],
                                                                  width_resolution, height_resolution)
        except Exception:
            log.exception('An error occurred while trying to generate the preview image.')

        return layer_preview_url

    def compose_map(self, request, resource_id, scenario_id, *args, **kwargs):
        """
        Compose the MapView object.

        Args:
            scenario_id (int): ID of the scenario.

        Returns:
            MapView, 4-list, list: The MapView, map extent, and layer groups.
        """
        # Get endpoint
        endpoint = self.get_wms_endpoint()

        # Get default view and extent for model
        view, model_extent = self.get_map_extent()

        layers = []
        vector_layers = []
        raster_layers = []
        index_maps = []
        lnd_layers = []

        # Boundary
        layer = self.compose_model_boundary_layer(endpoint, scenario_id)
        layers.append(layer)
        vector_layers.append(layer)

        # Stream Links
        layer = self.compose_stream_links_layer(endpoint, scenario_id)
        layers.append(layer)
        vector_layers.append(layer)

        # Stream Nodes
        layer = self.compose_stream_nodes_layer(endpoint, scenario_id)
        layers.append(layer)
        vector_layers.append(layer)

        # Link/Node Datasets
        layer = self.compose_link_node_layers(endpoint, scenario_id)
        layers.extend(layer)
        lnd_layers.extend(layer)

        # Elevation
        layer = self.compose_elevation_layer(endpoint, scenario_id)
        layers.append(layer)
        raster_layers.append(layer)

        # Index Maps
        layer = self.compose_index_map_layers(endpoint, scenario_id)
        layers.extend(layer)
        index_maps.extend(layer)

        # Mask
        layer = self.compose_mask_map_layer(endpoint, scenario_id)
        layers.append(layer)
        raster_layers.append(layer)

        # Define Layer Groups
        layer_groups = [
            self.build_layer_group(
                id='feature_layers',
                display_name='Features',
                layers=vector_layers
            ),
            self.build_layer_group(
                id='raster_layers',
                display_name='Maps',
                layers=raster_layers,
                layer_control='radio',
                visible=False
            ),
            self.build_layer_group(
                id='index_maps',
                display_name='Index Maps',
                layers=index_maps,
                layer_control='radio',
                visible=False
            )
        ]

        if lnd_layers:
            layer_groups.append(self.build_layer_group(
                id='lnd_layers',
                display_name='Link-Node Datasets',
                layers=lnd_layers,
                layer_control='radio',
                visible=False
            ))

        # Get api key for basemaps
        BING_API_KEY = app.get_custom_setting('bing_api_key')

        if BING_API_KEY:
            basemaps = [{
                'Bing': {'key': BING_API_KEY,
                         'imagerySet': 'AerialWithLabels',
                         'label': 'Aerial w/Labels'}
            }, {
                'Bing': {'key': BING_API_KEY,
                         'imagerySet': 'Aerial',
                         'label': 'Aerial'}
            }, {
                'Bing': {'key': BING_API_KEY,
                         'imagerySet': 'Road',
                         'label': 'Road'}
            }]
        else:
            basemaps = []

        MapView.ol_version = self.MAP_VIEW_VERSION

        map_view = MapView(
            height='600px',
            width='100%',
            controls=['ZoomSlider', 'Rotate', 'FullScreen'],
            layers=layers,
            view=view,
            basemap=basemaps,
            legend=True
        )

        return map_view, model_extent, layer_groups

    def compose_model_boundary_layer(self, endpoint, scenario_id):
        """
        Compose layer object for the model boundary layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_MODEL_BOUNDARY,
            model_db=self.model_db,
            with_workspace=True
        )

        layer_title = self.spatial_manager.VL_MODEL_BOUNDARY.replace('_', ' ').title()

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=self.spatial_manager.VL_MODEL_BOUNDARY,
            viewparams=viewparams,
            visible=True,
            selectable=True,
        )

        return mv_layer

    def compose_stream_links_layer(self, endpoint, scenario_id):
        """
        Compose layer object for the stream links layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_STREAM_LINKS,
            model_db=self.model_db,
            with_workspace=True
        )
        layer_title = self.spatial_manager.VL_STREAM_LINKS.replace('_', ' ').title()

        # Compose env
        units = ''  #: Default variable shown for stream links is link id, so no units.
        env = self.build_param_string(units=units)

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=self.spatial_manager.VL_STREAM_LINKS,
            viewparams=viewparams,
            env=env,
            visible=True,
            selectable=True,
        )

        return mv_layer

    def compose_stream_nodes_layer(self, endpoint, scenario_id):
        """
        Compose layer object for the stream nodes layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_STREAM_NODES,
            model_db=self.model_db,
            with_workspace=True
        )

        layer_title = self.spatial_manager.VL_STREAM_NODES.replace('_', ' ').title()

        # Compose env
        units = ''  #: Default variable shown for stream nodes is node id, so no units.
        env = self.build_param_string(units=units)

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=self.spatial_manager.VL_STREAM_NODES,
            viewparams=viewparams,
            env=env,
            visible=False,
            selectable=True,
            plottable=True
        )

        return mv_layer

    def compose_link_node_layers(self, endpoint, scenario_id):
        """
        Compose layer objects for each link node layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            list<MVLayer>: list of layer objects.
        """
        mv_layers = []
        model_db_session = None

        try:
            # Get all the link node dataset file names
            model_db_session = self.model_db.get_session()

            link_node_datasets = model_db_session.query(LinkNodeDatasetFile). \
                filter(LinkNodeDatasetFile.projectFileID == scenario_id). \
                all()

            for link_node_dataset in link_node_datasets:
                # Compose layer name
                layer_name = self.spatial_manager.get_unique_item_name(
                    item_name=self.spatial_manager.VL_LINK_NODE,
                    suffix=link_node_dataset.fileExtension,
                    model_db=self.model_db,
                    with_workspace=True
                )

                if link_node_dataset.fileExtension in self.LND_DISPLAY_NAMES:
                    layer_title = self.LND_DISPLAY_NAMES[link_node_dataset.fileExtension]
                else:
                    layer_title = link_node_dataset.name

                # Compose viewparams
                time_summary = 'Max'
                viewparams = self.build_param_string(
                    scenarioid=scenario_id,
                    timesummary=time_summary
                )

                # Compose env
                units = ''  # TODO: Compute custom units
                env = self.build_param_string(units=units)
                # TODO: Compute custom color ramp for based on min/max and cache as users setting?
                # DEFAULT IN SLD IS:
                # --------------- color1 #77239D
                # division1 0.01
                # --------------- color2 #391B95
                # division2 0.1
                # --------------- color3 #0057D5
                # division3 1.0
                # --------------- color4 #038DBB
                # division4 2.0
                # --------------- color5 #649C31
                # division5 3.0
                # --------------- color6 #F4ED01
                # division6 4.0
                # --------------- color7 #D38306
                # division7 5.0
                # --------------- color8 #E12300

                # Compose layer
                mv_layer = self.build_wms_layer(
                    endpoint=endpoint,
                    layer_name=layer_name,
                    layer_title=layer_title,
                    layer_variable=layer_title.lower().replace(' ', '_'),
                    viewparams=viewparams,
                    env=env,
                    visible=False
                )

                mv_layers.append(mv_layer)
        finally:
            model_db_session and model_db_session.close()

        return mv_layers

    def compose_elevation_layer(self, endpoint, scenario_id):
        """
        Compose layer object for the elevation layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            MVLayer: layer object.
        """
        model_db_session = None

        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.RL_ELEVATION,
            model_db=self.model_db,
            scenario_id=scenario_id,
            with_workspace=True
        )

        layer_title = self.spatial_manager.RL_ELEVATION.replace('_', ' ').title()

        # Compose env
        # TODO: Cache as user setting?
        # DEFAULT IN SLD IS:
        # color0  #96D257  val_no_data 0  (opacity = 0% - transparent)
        # color0  #96D257  val0  0  0.00001
        # color1  #278C39  val1  1  10
        # color2  #2A7B45  val2  2  20
        # color3  #829C41  val3  3  30
        # color4  #DBB82E  val4  4  40
        # color5  #AE4818  val5  5  50
        # color6  #842511  val6  6  60
        # color7  #61370F  val7  7  70
        # color8  #806346  val8  8  80
        # color9  #C2C2C2  val9  9  90
        # color10 #FFFFFF  val10 10 100
        stats = {'min': 1, 'max': 5000}

        try:
            model_db_session = self.model_db.get_session()

            elevation_raster = model_db_session.query(RasterMapFile). \
                filter(RasterMapFile.projectFileID == scenario_id). \
                filter(RasterMapFile.fileExtension == 'ele'). \
                one_or_none()

            if elevation_raster is not None:
                # Compute stats of elevation raster
                stats = compute_raster_stats(
                    session=model_db_session,
                    raster_table=RasterMapFile.__tablename__,
                    id=elevation_raster.id
                )

            # No minimum values less than zero for elevation ramp
            stats['min'] = stats['min'] if stats['min'] >= 1 else 1

        finally:
            model_db_session and model_db_session.close()

        # Compute custom divisions
        divisions = self.generate_custom_color_ramp_divisions(
            min_value=stats['min'],
            max_value=stats['max'],
            num_divisions=10
        )

        env = self.build_param_string(**divisions)

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=self.spatial_manager.RL_ELEVATION,
            env=env,
            visible=False
        )

        return mv_layer

    def compose_mask_map_layer(self, endpoint, scenario_id):
        """
        Compose layer object for the mask layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.RL_MASK,
            model_db=self.model_db,
            scenario_id=scenario_id,
            with_workspace=True
        )

        layer_title = self.spatial_manager.RL_MASK.replace('_', ' ').title()

        # Compose env
        # TODO: Cache as user setting?
        # DEFAULT IN SLD IS:
        # inactive_color  #000000  inactive_val 0  (opacity = 0% - transparent)
        # active_color    #000000  active_val   1

        env = self.build_param_string()

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title=layer_title,
            layer_variable=self.spatial_manager.RL_MASK,
            env=env,
            visible=False
        )

        return mv_layer

    def compose_index_map_layers(self, endpoint, scenario_id):
        """
        Compose layer objects for each index map layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            scenario_id (int): ID of the scenario.
        Returns:
            list<MVLayer>: list of layer objects.
        """
        mv_layers = []
        model_db_session = None

        try:
            model_db_session = self.model_db.get_session()

            project_file = model_db_session.query(ProjectFile).get(scenario_id)
            map_table_file = project_file.mapTableFile
            index_maps = model_db_session.query(IndexMap). \
                filter(IndexMap.mapTableFileID == map_table_file.id). \
                all()

            for index_map in index_maps:
                # Compose layer name
                layer_name = self.spatial_manager.get_unique_item_name(
                    item_name=self.spatial_manager.RL_INDEX,
                    suffix=index_map.name.replace(' ', '_'),
                    model_db=self.model_db,
                    scenario_id=scenario_id,
                    with_workspace=True
                )

                # Compose env
                # TODO: Cache as user setting?
                # DEFAULT IN SLD IS:
                # color_no_data   #E12300  val_no_data 0
                # color1   #E12300  val1   1
                # color2   #D38306  val2   2
                # color3   #F4ED01  val3   3
                # color4   #649C31  val4   4
                # color5   #038DBB  val5   5
                # color6   #0057D5  val6   6
                # color7   #391B95  val7   7
                # color8   #77239D  val8   8
                # color9   #FE634D  val9   9
                # color10  #FFB23C  val10  10
                # color11  #FBF968  val11  11
                # color12  #97D45F  val12  12
                # color13  #00C7FF  val13  13
                # color14  #3689FF  val14  14
                # color15  #5A32EB  val15  15
                # color16  #BC37F2  val16  16
                # color17  #FCB5AF  val17  17
                # color18  #FFD8A8  val18  18
                # color19  #FFFCB5  val19  19
                # color20  #CDE9B8  val20  20
                # color21  #90E4FE  val21  21
                # color22  #AAC4FD  val22  22
                # color23  #B28CFB  val23  23
                # color24  #E395FB  val24  24
                # color25  #FE4310  val25  25
                # color26  #FFAA00  val26  26
                # color27  #FDFB44  val27  27
                # color28  #75BA43  val28  28
                # color29  #00A2D8  val29  29
                # color30  #0460FF  val30  30
                # color31  #4A24B7  val31  31
                # color32  #9A2ABA  val32  32
                # color33  #B51902  val33  33
                # color34  #AB6702  val34  34
                # color35  #C2BD00  val35  35
                # color36  #4C7C28  val36  36
                # color37  #00728B  val37  37
                # color38  #0142A6  val38  38
                # color39  #2C1378  val39  39
                # color40  #63167E  val40  40
                # color41  #FF8C85  val41  41
                # color42  #FFC878  val42  42
                # color43  #FDFA91  val43  43
                # color44  #B0DC87  val44  44
                # color45  #55D6FE  val45  45
                # color46  #75A7FE  val46  46
                # color47  #854FFB  val47  47
                # color48  #D456FF  val48  48
                # color49  #FFD8D9  val49  49
                # color50  #FFEBD3  val50  50
                # color51  #FFFCDB  val51  51
                # color52  #E2EBDA  val52  52
                # color53  #CAF2FE  val53  53
                # color54  #D4E4FB  val54  54
                # color55  #DACAFB  val55  55
                # color56  #F1C9FE  val56  56
                # color57  #830D00  val57  57
                # color58  #794803  val58  58
                # color59  #888901  val59  59
                # color60  #3B571C  val60  60
                # color61  #004B63  val61  61
                # color62  #013078  val62  62
                # color63  #180B51  val63  63
                # color64  #450F5D  val64  64
                # color65  #FF0000  val65  65
                # color66  #FF8000  val66  66
                # color67  #FFFF00  val67  67
                # color68  #00FF00  val68  68
                # color69  #00FFFF  val69  69
                # color70  #0000FF  val70  70
                # color71  #8000FF  val71  71
                # color72  #800000  val72  72
                # color73  #804000  val73  73
                # color74  #808000  val74  74
                # color75  #008000  val75  75
                # color76  #008080  val76  76
                # color77  #000080  val77  77
                # color78  #400080  val78  78
                # color79  #FF2A00  val79  79
                # color80  #FFAA00  val80  80
                # color81  #AAFF00  val81  81
                # color82  #00FF55  val82  82
                # color83  #00AAFF  val83  83
                # color84  #2A00FF  val84  84
                # color85  #8000AA  val85  85
                # color86  #801500  val86  86
                # color87  #805500  val87  87
                # color88  #558000  val88  88
                # color89  #00802A  val89  89
                # color90  #005580  val90  90
                # color91  #150080  val91  91
                # color92  #FF5500  val92  92
                # color93  #FFD400  val93  93
                # color94  #55FF00  val94  94
                # color95  #00FFAA  val95  95
                # color96  #0055FF  val96  96
                # color97  #5500FF  val97  97
                # color98  #800055  val98  98
                # color99  #802A00  val99  99
                # color100 #806A00  val100 100
                # color101 #2A8000  val101 101
                # color102 #008055  val102 102
                # color103 #002A80  val103 103
                # color104 #2A0080  val104 104
                env = self.build_param_string()

                # Compose layer
                mv_layer = self.build_wms_layer(
                    endpoint=endpoint,
                    layer_name=layer_name,
                    layer_title=index_map.name,
                    layer_variable=index_map.name.lower().replace(' ', '_'),
                    env=env,
                    visible=False
                )

                mv_layers.append(mv_layer)
        finally:
            model_db_session and model_db_session.close()

        return mv_layers

    def get_plot_for_layer_feature(self, layer_name, feature_id):
        """
        Get plot data for given feature on given layer.

        Args:
            layer_name(str): Name/id of layer.
            feature_id(str): PostGIS Feature ID of feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
        """
        # TODO: FINISH DEFAULT IMPLEMENTATION USE FEATURE ID IN POSTGIS QUERY TO FIND MATCHING ID IN DATABASE
        # TODO: TEST THIS AFTER IMPLEMENTED
        title = 'Fake Plot'
        layout = {
            'xaxis': {
                'title': layer_name
            },
            'yaxis': {
                'title': 'Value (units)'
            }
        }

        series1 = {
            'name': feature_id + '1',
            'mode': 'lines',
            'x': [1, 2, 3, 4],
            'y': [10, 15, 13, 17],
        }

        series2 = {
            'name': feature_id + '2',
            'mode': 'lines',
            'x': [1, 2, 3, 4],
            'y': [15, 20, 8, 12],
        }

        data = [series1, series2]

        return title, data, layout