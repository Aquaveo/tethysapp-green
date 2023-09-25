from tethys_sdk.gizmos import MapView, MVLayer, MVView
from tethysext.atcore.services.map_manager import MapManagerBase
from tethysapp.green.app import Green as app
from gsshapyorm.orm.map import RasterMapFile

import numpy as np

class ModelMapManager(MapManagerBase):
    """
    Object that orchestrates the map layers and resources for Green app.
    """
    MAP_VIEW_VERSION = '4.6.5'
    MAX_ZOOM = 28
    MIN_ZOOM = 4
    DEFAULT_ZOOM = 13
    DEFAULT_EXTENT = [-125, 24, -65, 50]

    def get_map_extent(self):
        """
        Get the default view and extent for the project.

        Returns:
            MVView, 4-list<float>: default view and extent of the project.
        """
        extent = self.DEFAULT_EXTENT

        # Compute center
        center = self.DEFAULT_CENTER
        if extent and len(extent) >= 4:
            center_x = (extent[0] + extent[2]) / 2.0
            center_y = (extent[1] + extent[3]) / 2.0
            center = [center_x, center_y]

        # Construct the default view
        view = MVView(
            projection='EPSG:4326',
            center=center,
            zoom=self.DEFAULT_ZOOM,
            maxZoom=self.MAX_ZOOM,
            minZoom=self.MIN_ZOOM
        )

        return view, extent

    def compose_map(self, request, *args, **kwargs):
        """
        Compose the MapView object.
        Args:
            request(HttpRequest): A Django request object.

        Returns:
            MapView, 4-list<float>: The MapView and extent objects.
        """
        from tethysext.atcore.models.app_users import AppUser
        from tethysext.atcore.services.model_database import ModelDatabase
        from tethysapp.green.models import GsshaModel

        session = app.get_persistent_store_database(app.DATABASE_NAME, as_sessionmaker=True)()

        print(kwargs['resource_id'])

        try:
            request_app_user = AppUser.get_app_user_from_request(request, session)

            gssha_models = request_app_user.get_resources(
                session=session,
                request=request,
                of_type=GsshaModel,
            )

            # Get endpoint
            endpoint = self.get_wms_endpoint()

            # Get default view and extent for model
            view, model_extent = self.get_map_extent()

            layers = []

            for gssha_model in gssha_models:
                if gssha_model.id != kwargs['resource_id']:
                 #   print()
                    continue
                database_id = gssha_model.get_attribute('database_id')
              #  print(gssha_model.get_attribute('id'),dir(gssha_model))
                print(gssha_model.id)
                if not database_id:
                    continue
                model_db = ModelDatabase(app=app, database_id=database_id)

                # Compose model boundary layer
                model_boundary_layer = self.compose_model_boundary_layer(
                    endpoint=endpoint,
                    model_db=model_db,
                    scenario_id=self.spatial_manager.BASE_SCENARIO_ID,
                    gssha_model=gssha_model,
                )
                model_stream_layer = self.compose_model_stream_layer(
                    endpoint=endpoint,
                    model_db=model_db,
                    scenario_id=self.spatial_manager.BASE_SCENARIO_ID,
                    gssha_model=gssha_model,
                )
                model_node_layer = self.compose_model_node_layer(
                    endpoint=endpoint,
                    model_db=model_db,
                    scenario_id=self.spatial_manager.BASE_SCENARIO_ID,
                    gssha_model=gssha_model,
                )
                model_ele_layer = self.compose_model_ele_layer(
                    endpoint=endpoint,
                    model_db=model_db,
                    scenario_id=self.spatial_manager.BASE_SCENARIO_ID,
                    gssha_model=gssha_model,
                )


                layers.append(model_ele_layer)
                layers.append(model_boundary_layer)
                layers.append(model_stream_layer)
                layers.append(model_node_layer)


            # Define Layer Groups
            layer_groups = [
                self.build_layer_group(
                    id='gssha_layers',
                    display_name='GSSHA Models',
                    layers=layers
                ),
            ]

            MapView.ol_version = self.MAP_VIEW_VERSION

            map_view = MapView(
                height='600px',
                width='100%',
                controls=['ZoomSlider', 'Rotate', 'FullScreen'],
                layers=layers,
                view=view,
                basemap=[],
                legend=True
            )

        finally:
            session.close()

        return map_view, model_extent, layer_groups

    def get_cesium_token(self):
        """
        Get the cesium token for Cesium Views

        Returns:
            str: The cesium API token
        """
        return app.get_custom_setting('cesium_api_key')

    def compose_model_boundary_layer(self, endpoint, model_db, scenario_id, gssha_model):
        """
        Compose layer object for the model boundary layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            model_db (ModelDatabase): Model database for the gssha model.
            scenario_id (int): ID of the scenario.
            gssha_model (GsshaModel): GSSHA model Resource object.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_MODEL_BOUNDARY,
            model_db=model_db,
            with_workspace=True
        )

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Get extent for gssha model
        extent = self.spatial_manager.get_extent_for_project(
            model_db=model_db,
        )

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title="Boundary",
            layer_variable=self.spatial_manager.VL_MODEL_BOUNDARY,
            extent=extent,
            viewparams=viewparams,
            visible=True,
            selectable=True,
        )

        return mv_layer

    def compose_model_stream_layer(self, endpoint, model_db, scenario_id, gssha_model):
        """
        Compose layer object for the model boundary layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            model_db (ModelDatabase): Model database for the gssha model.
            scenario_id (int): ID of the scenario.
            gssha_model (GsshaModel): GSSHA model Resource object.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_STREAM_LINKS,
            model_db=model_db,
            with_workspace=True
        )

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Get extent for gssha model
        extent = self.spatial_manager.get_extent_for_project(
            model_db=model_db,
        )

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title="Streams",
            layer_variable=self.spatial_manager.VL_STREAM_LINKS,
            extent=extent,
            viewparams=viewparams,
            visible=True,
            selectable=True,
        )

        return mv_layer

    def compose_model_node_layer(self, endpoint, model_db, scenario_id, gssha_model):
        """
        Compose layer object for the model boundary layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            model_db (ModelDatabase): Model database for the gssha model.
            scenario_id (int): ID of the scenario.
            gssha_model (GsshaModel): GSSHA model Resource object.
        Returns:
            MVLayer: layer object.
        """
        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.VL_STREAM_NODES,
            model_db=model_db,
            with_workspace=True
        )

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)

        # Get extent for gssha model
        extent = self.spatial_manager.get_extent_for_project(
            model_db=model_db,
        )

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title="Nodes",
            layer_variable=self.spatial_manager.VL_STREAM_NODES,
            extent=extent,
            viewparams=viewparams,
            visible=True,
            selectable=True,
        )

        return mv_layer

    def compose_model_ele_layer(self, endpoint, model_db, scenario_id, gssha_model):
        """
        Compose layer object for the model boundary layer.

        Args:
            endpoint (str): URL of geoserver wms service.
            model_db (ModelDatabase): Model database for the gssha model.
            scenario_id (int): ID of the scenario.
            gssha_model (GsshaModel): GSSHA model Resource object.
        Returns:
            MVLayer: layer object.
        """

        #TODO:Query/Find elevation values to set range of raster style in env parameters


        # Compose layer name
        layer_name = self.spatial_manager.get_unique_item_name(
            item_name=self.spatial_manager.RL_ELEVATION,
            model_db=model_db,
            with_workspace=True,
            scenario_id=1,
        )

        model_session = model_db.get_session_maker()()

        raster_map = model_session.query(RasterMapFile).filter(RasterMapFile.fileExtension == "ele").first()

        if raster_map:
            print(raster_map.rows)
            print(raster_map.rasterText)
            raster_max = getMaxFromRasterText(raster_map.rasterText)

            ramp = createRampFromMax(int(raster_max*0.5), raster_max*1.2, 10)

            rlist = [["val_no_data", 0.0]]
            rlist += [["val{0}".format(i),r] for i,r in enumerate(ramp)]
            print(rlist)



        model_session.close()

        # Compose viewparams
        viewparams = self.build_param_string(scenarioid=scenario_id)



        #make color and value env dictionary
        env_dict = {
            "color0":"#000000"
        }



        for r in rlist:
            env_dict[r[0]] = r[1]


        # TODO
        # Compose envparams (color0, color1, value0, value1, etc.)
        # Compose viewparams
        envparams = self.build_param_string(**env_dict)

        # Get extent for gssha model
        extent = self.spatial_manager.get_extent_for_project(
            model_db=model_db,
        )

        print("LAYER: ", layer_name)

        # Compose layer
        mv_layer = self.build_wms_layer(
            endpoint=endpoint,
            layer_name=layer_name,
            layer_title="elevation",
            layer_variable=self.spatial_manager.RL_ELEVATION,
            extent=extent,
            viewparams=viewparams,
            env=envparams,
            visible=True,
            selectable=True,
        )

        return mv_layer



def getMaxFromRasterText(raster_text):
    lines = raster_text.split('\n')

    raster_max = 0

    for l in lines:
        if ":" not in l:
            try:
                raster_new_max = max([float(x) for x in l.split(" ")[:-1]])
                if raster_new_max > raster_max:
                    raster_max = raster_new_max
            except Exception as e:
                print(e)
                for x in l.split(" ")[:-1]:
                    print("x is: {0}".format(x))
                print([float(x) for x in l.split(" ")[:-1] if not x.isspace()])

    print("Max is {0}".format(raster_max))

    return raster_max

def createRampFromMax(start=0, stop=100, increment=10):
    ramp = []
    for x in range(start, int(stop), int((stop-start)/increment))[1:]:
        ramp.append(x)

    ramp.insert(0,0.001)

    return ramp
