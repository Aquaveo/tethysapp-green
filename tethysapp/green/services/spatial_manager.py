import os
import tempfile
import zipfile
from jinja2 import Template
from gsshapyorm.orm import ProjectFile, IndexMap, LinkNodeDatasetFile
from tethysext.atcore.services.model_db_spatial_manager import ModelDBSpatialManager
from tethysext.atcore.services.base_spatial_manager import reload_config


class GsshaSpatialManager(ModelDBSpatialManager):
    """
    Managers GeoServer Layers for GSSHA Projects.
    """
    WORKSPACE = 'green'
    URI = 'http://umip.erdc.dren.mil/green'
    BASE_SCENARIO_ID = 1
    SQL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'sql_templates')
    SLD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'sld_templates')

    # Vector Layer Types
    VL_MODEL_BOUNDARY = 'model_boundary'
    VL_STREAM_LINKS = 'stream_links'
    VL_STREAM_NODES = 'stream_nodes'
    VL_LINK_NODE = 'stream_link_node'

    # Raster Layer Types
    RL_ELEVATION = 'elevation'
    RL_MASK = 'mask'
    RL_INDEX = 'index'

    # Link Node Dataset Variables
    LN_STREAM_DEPTH = 'cdp'
    LN_STREAM_FLOW = 'cdq'
    VALID_LINK_NODE_VARIABLES = (LN_STREAM_DEPTH, LN_STREAM_FLOW)

    LOGARITHMIC_DIVISIONS = {
        'division1_default': 0.01,
        'division2_default': 0.1,
        'division3_default': 1.0,
        'division4_default': 10.0,
        'division5_default': 100.0,
        'division6_default': 1000.0,
        'division7_default': 10000.0,
    }

    LN_DEFAULT_DIVISIONS = {
        LN_STREAM_DEPTH: {
            'division1_default': 0.01,
            'division2_default': 0.1,
            'division3_default': 1.0,
            'division4_default': 2.0,
            'division5_default': 3.0,
            'division6_default': 4.0,
            'division7_default': 5.0,
        },
        LN_STREAM_FLOW: LOGARITHMIC_DIVISIONS
    }

    def get_extent_for_project(self, model_db):
        """
        Return the extent / bounding box for a project.
        Args:
            model_db (ModelDatabase): the object representing the model database.
        Returns:
            4-list: Extent bounding box (e.g.: [minx, miny, maxx, maxy] ).
        """
        mask_raster_layer = self.get_unique_item_name(
            item_name=self.VL_MODEL_BOUNDARY,
            model_db=model_db
        )

        extent = self.gs_engine.get_layer_extent(
            store_id=f"{self.WORKSPACE}:{model_db.get_id()}",
            feature_name=mask_raster_layer
        )

        return extent

    @reload_config()
    def create_all_layers(self, model_db, srid, project_dir, scenario_id=BASE_SCENARIO_ID,
                          with_link_node_datasets=False, for_scenario=False, reload_config=True):
        """
        High level function to create all GeoServer layers for the gssha project.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            project_dir(str): Path to the GSSHA project directory containing the rasters (i.e.: *.ele, *.msk, *.idx).
            with_link_node_datasets(bool): Create link node dataset layers. Defaults to False.
            for_scenario(bool): Create the subset of layers required for a scenario (i.e. non-dynamic layers). Defaulst to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """  # noqa:E501
        # Vector layers are tied to the database and are dynamic, so we don't need to recreate them
        if not for_scenario:
            # Vector
            self.create_all_vector_layers(
                model_db=model_db,
                srid=srid,
                reload_config=False
            )

        # Raster
        self.create_all_raster_layers(
            model_db=model_db,
            scenario_id=scenario_id,
            srid=srid,
            project_dir=project_dir,
            reload_config=False
        )

        # Link Node
        if with_link_node_datasets:
            self.create_all_link_node_dataset_layers(
                model_db=model_db,
                scenario_id=scenario_id,
                srid=srid,
                reload_config=False
            )

    @reload_config()
    def delete_all_layers(self, model_db, scenario_id=BASE_SCENARIO_ID, with_link_node_datasets=False,
                          reload_config=True):
        """
        High level function to delete all GeoServer layers for the gssha project.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            with_link_node_datasets(bool): Delete link node dataset layers. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        if scenario_id == self.BASE_SCENARIO_ID:
            # Vector
            self.delete_all_vector_layers(
                model_db=model_db,
                reload_config=False
            )

            # Link Node
            if with_link_node_datasets:
                self.delete_all_link_node_dataset_layers(
                    model_db=model_db,
                    reload_config=False
                )

        # Raster
        self.delete_all_raster_layers(
            model_db=model_db,
            scenario_id=scenario_id,
            reload_config=False
        )

    @reload_config()
    def create_all_styles(self, overwrite=False, reload_config=True):
        """
        High level function to create all GeoServer styles.

        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Model Boundary
        self.create_model_boundary_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Stream Links
        self.create_stream_links_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Stream Nodes
        self.create_stream_nodes_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Elevation
        self.create_elevation_raster_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Mask
        self.create_mask_raster_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Index
        self.create_index_map_raster_styles(
            overwrite=overwrite,
            reload_config=False
        )

        # Link Node
        for variable in self.VALID_LINK_NODE_VARIABLES:
            self.create_link_node_dataset_styles(
                variable=variable,
                overwrite=overwrite,
                reload_config=False
            )

    @reload_config()
    def delete_all_styles(self, purge=True, reload_config=True):
        """
        High level function to delete all GeoServer styles.

        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Model Boundary
        self.delete_model_boundary_styles(
            purge=purge,
            reload_config=False
        )

        # Stream Links
        self.delete_stream_links_styles(
            purge=purge,
            reload_config=False
        )

        # Stream Nodes
        self.delete_stream_nodes_styles(
            purge=purge,
            reload_config=False
        )

        # Elevation
        self.delete_elevation_raster_styles(
            purge=purge,
            reload_config=False
        )

        # Mask
        self.delete_mask_raster_styles(
            purge=purge,
            reload_config=False
        )

        # Index
        self.delete_index_map_raster_styles(
            purge=purge,
            reload_config=False
        )

        # Link Node
        for variable in self.VALID_LINK_NODE_VARIABLES:
            self.delete_link_node_dataset_styles(
                variable=variable,
                purge=purge,
                reload_config=False
            )

    @reload_config()
    def create_all_vector_layers(self, model_db, srid, reload_config=True):
        """
        High level method to create all GeoServer vector layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Boundary
        self.create_model_boundary_layer(
            model_db=model_db,
            srid=srid,
            reload_config=False
        )

        # Stream Links
        self.create_stream_links_layer(
            model_db=model_db,
            srid=srid,
            reload_config=False
        )

        # Stream Nodes
        self.create_stream_nodes_layer(
            model_db=model_db,
            srid=srid,
            reload_config=False
        )

    @reload_config()
    def delete_all_vector_layers(self, model_db, reload_config=True):
        """
        High level method to delete all GeoServer vector layers.

        Args:
           model_db(ModelDatabase): the object representing the models database.
           recurse(bool): recursively delete any dependent GeoServer objects if True.
           reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Boundary
        self.delete_model_boundary_layer(
            model_db=model_db,
            reload_config=False
        )

        # Stream Links
        self.delete_stream_links_layer(
            model_db=model_db,
            reload_config=False
        )

        # Stream Nodes
        self.delete_stream_nodes_layer(
            model_db=model_db,
            reload_config=False
        )

    @reload_config()
    def create_all_raster_layers(self, model_db, srid, project_dir, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        High level method to create all GeoServer raster layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            project_dir(str): Path to the GSSHA project directory containing the rasters (i.e.: *.ele, *.msk, *.idx).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        if not os.path.exists(project_dir) or not os.path.isdir(project_dir):
            raise IOError('"{}" is not a valid directory.'.format(project_dir))

        # Get project file from models database
        session = model_db.get_session()
        try:
            project_file = session.query(ProjectFile).get(scenario_id)

            # Get name of elevation and mask raster from project cards
            elevation_raster_card = project_file.getCard('ELEVATION')
            mask_raster_card = project_file.getCard('WATERSHED_MASK')

            elevation_raster_filename = elevation_raster_card.value if elevation_raster_card else ''
            mask_raster_filename = mask_raster_card.value if mask_raster_card else ''

            # Clean up names
            elevation_raster_filename = elevation_raster_filename.replace('"', '').replace("'", '')
            mask_raster_filename = mask_raster_filename.replace('"', '').replace("'", '')

            index_maps = session.query(IndexMap).\
                filter(IndexMap.mapTableFileID == project_file.mapTableFileID).\
                all()

            index_map_filenames = []
            for index_map in index_maps:
                index_map_filenames.append(index_map.filename)

        finally:
            session.close()

        # Elevation
        elevation_path = os.path.join(project_dir, elevation_raster_filename)
        if os.path.isfile(elevation_path):
            self.create_elevation_raster_layer(
                model_db=model_db,
                scenario_id=scenario_id,
                srid=srid,
                raster_map_file=elevation_path,
                reload_config=False
            )

        # Mask
        mask_path = os.path.join(project_dir, mask_raster_filename)
        if os.path.isfile(mask_path):
            self.create_mask_raster_layer(
                model_db=model_db,
                scenario_id=scenario_id,
                srid=srid,
                raster_map_file=mask_path,
                reload_config=False
            )

        # Index
        index_map_paths = []
        for index_map_filename in index_map_filenames:
            index_map_path = os.path.join(project_dir, index_map_filename)
            if os.path.isfile(index_map_path):
                index_map_paths.append(index_map_path)

        if index_map_paths:
            self.create_all_index_map_raster_layers(
                model_db=model_db,
                scenario_id=scenario_id,
                srid=srid,
                raster_map_files=index_map_paths,
                reload_config=False
            )

    @reload_config()
    def delete_all_raster_layers(self, model_db, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        High level method to delete all GeoServer raster layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Elevation
        self.delete_elevation_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            reload_config=False
        )

        # Mask
        self.delete_mask_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            reload_config=False
        )

        # Index
        self.delete_all_index_map_raster_layers(
            model_db=model_db,
            scenario_id=scenario_id,
            reload_config=False
        )

    @reload_config()
    def create_all_link_node_dataset_layers(self, model_db, srid, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        High level method to create all GeoServer link node dataset layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            scenario_id(int): id of the scenario.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """  # noqa: E501
        session = model_db.get_session()
        try:
            link_node_datasets = session.\
                query(LinkNodeDatasetFile).\
                filter(LinkNodeDatasetFile.projectFileID == scenario_id).\
                filter(LinkNodeDatasetFile.channelInputFileID.isnot(None)).\
                all()

            variables = []
            for link_node_dataset in link_node_datasets:
                variables.append(link_node_dataset.fileExtension)

        finally:
            session.close()

        for variable in variables:
            self.create_link_node_dataset_layer(
                model_db=model_db,
                variable=variable,
                srid=srid,
                reload_config=False
            )

    @reload_config()
    def delete_all_link_node_dataset_layers(self, model_db, recurse=True, reload_config=True):
        """
        High level method to delete all GeoServer link node dataset layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            recurse(bool): recursively delete any dependent GeoServer objects if True.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """  # noqa: E501
        for variable in self.VALID_LINK_NODE_VARIABLES:
            self.delete_link_node_dataset_layer(
                model_db=model_db,
                variable=variable,
                recurse=recurse,
                reload_config=False
            )

    def get_unique_item_name(self, item_name, variable='', suffix='', model_db=None, scenario_id=None,
                             with_workspace=False):
        """
        Construct the unique name for the specific item.

        Args:
            item_name(str): name of item.
            variable(str): Variable name.
            suffix(str): suffix to append to name (e.g.: 'labels').
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): the id of the scenario.
            with_workspace(bool): include the workspace if True. Defaults to False.

        Returns:
            str: unique name for item.
        """
        # e.g.: <model_id>_<scenario_id>_<item_name>_<suffix>
        name_parts = []

        if model_db is not None:
            name_parts.append(model_db.get_id().replace('_', '-'))

        if scenario_id is not None:
            name_parts.append(str(scenario_id))

        name_parts.append(str(item_name))

        if variable:
            name_parts.append(variable)

        # e.g.: 88c1b4ce-7def-43fd-b19f-1fca8fea282d_model_boundary_legend
        if suffix:
            name_parts.append(suffix)

        name = '_'.join(name_parts)

        if with_workspace:
            return '{0}:{1}'.format(self.WORKSPACE, name)

        return name

    @reload_config()
    def create_model_boundary_layer(self, model_db, srid=3857, reload_config=True):
        """
        Creates a GeoServer SQLView Layer for the models boundary derived from the mask raster.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Get Layer Name
        layer_name = self.get_unique_item_name(item_name=self.VL_MODEL_BOUNDARY, model_db=model_db)

        # Get Default Style Name
        default_style = self.get_unique_item_name(self.VL_MODEL_BOUNDARY)

        # Determine units
        units = self.get_projection_units(model_db=model_db, srid=srid)
        boundary_raster = 'msk'

        sql_context = {
            'boundary_raster': boundary_raster,
            'units': units
        }

        # Render SQL
        sql_template_file = os.path.join(self.SQL_PATH, self.VL_MODEL_BOUNDARY + '.sql')
        with open(sql_template_file, 'r') as sql_template_file:
            text = sql_template_file.read()
            template = Template(text)
            sql = ' '.join(template.render(sql_context).split())

        # Create SQL View
        self.gs_engine.create_sql_view_layer(
            store_id=f"{self.WORKSPACE}:{model_db.get_id()}",
            layer_name=layer_name,
            geometry_type=self.GT_POLYGON,
            srid=srid,
            sql=sql,
            default_style=default_style,
            parameters=(
                {
                    'name': 'scenarioid',
                    'default_value': '1',
                    'regex_validator': '^[0-9]+$'
                },
            )
        )

    @reload_config()
    def delete_model_boundary_layer(self, model_db, recurse=True, reload_config=True):
        """
        Deletes the GeoServer models boundary layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            recurse(bool): recursively delete any dependent GeoServer objects if True.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Get Layer Name
        layer_name = self.get_unique_item_name(item_name=self.VL_MODEL_BOUNDARY, model_db=model_db)
        self.gs_engine.delete_layer(
            layer_id=f"{self.WORKSPACE}:{layer_name}",
            datastore=model_db.get_id(),
            recurse=recurse
        )

    @reload_config()
    def create_stream_links_layer(self, model_db, srid=3857, reload_config=True):
        """
        Creates a GeoServer SQLView Layer for the stream links.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Get Layer Name
        layer_name = self.get_unique_item_name(item_name=self.VL_STREAM_LINKS, model_db=model_db)

        # Get Default Style Name
        default_style = self.get_unique_item_name(self.VL_STREAM_LINKS)

        # Render SQL
        sql_template_file = os.path.join(self.SQL_PATH, self.VL_STREAM_LINKS + '.sql')

        sql_context = {}

        with open(sql_template_file, 'r') as sql_template_file:
            text = sql_template_file.read()
            template = Template(text)
            sql = ' '.join(template.render(sql_context).split())

        # Create SQL View
        self.gs_engine.create_sql_view_layer(
            store_id=f"{self.WORKSPACE}:{model_db.get_id()}",
            layer_name=layer_name,
            geometry_type=self.GT_LINE,
            srid=srid,
            sql=sql,
            default_style=default_style,
            parameters=(
                {
                    'name': 'scenarioid',
                    'default_value': '1',
                    'regex_validator': '^[0-9]+$'
                },
            )
        )

    @reload_config()
    def delete_stream_links_layer(self, model_db, recurse=True, reload_config=True):
        """
        Deletes the GeoServer stream links layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            recurse(bool): recursively delete any dependent GeoServer objects if True.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        layer_name = self.get_unique_item_name(item_name=self.VL_STREAM_LINKS, model_db=model_db)
        self.gs_engine.delete_layer(
            layer_id=f"{self.WORKSPACE}:{layer_name}",
            datastore=model_db.get_id(),
            recurse=recurse
        )

    @reload_config()
    def create_stream_nodes_layer(self, model_db, srid=3857, reload_config=True):
        """
        Creates a GeoServer SQLView Layer for the stream nodes.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Get Layer Name
        layer_name = self.get_unique_item_name(item_name=self.VL_STREAM_NODES, model_db=model_db)

        # Get Default Style Name
        default_style = self.get_unique_item_name(self.VL_STREAM_NODES)

        # Render SQL
        sql_template_file = os.path.join(self.SQL_PATH, self.VL_STREAM_NODES + '.sql')

        sql_context = {}

        with open(sql_template_file, 'r') as sql_template_file:
            text = sql_template_file.read()
            template = Template(text)
            sql = ' '.join(template.render(sql_context).split())

        # Create SQL View
        self.gs_engine.create_sql_view_layer(
            store_id=f"{self.WORKSPACE}:{model_db.get_id()}",
            layer_name=layer_name,
            geometry_type=self.GT_POINT,
            srid=srid,
            sql=sql,
            default_style=default_style,
            parameters=(
                {
                    'name': 'scenarioid',
                    'default_value': '1',
                    'regex_validator': '^[0-9]+$'
                },
            )
        )

    @reload_config()
    def delete_stream_nodes_layer(self, model_db, recurse=True, reload_config=True):
        """
        Deletes the GeoServer stream nodes layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            recurse(bool): recursively delete any dependent GeoServer objects if True.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        layer_name = self.get_unique_item_name(item_name=self.VL_STREAM_NODES, model_db=model_db)
        self.gs_engine.delete_layer(
            layer_id=f"{self.WORKSPACE}:{layer_name}",
            datastore=model_db.get_id(),
            recurse=recurse
        )

    @reload_config()
    def create_link_node_dataset_layer(self, model_db, variable, srid=3857, reload_config=True):
        """
        Creates a GeoServer SQLView Layer for the link-node dataset variable specified.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            variable(str): the link node dataset variable. One of GsshaSpatialManager.LN_STREAM_FLOW or GsshaSpatialManager.LN_STREAM_DEPTH.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """  # noqa: E501
        if variable not in self.VALID_LINK_NODE_VARIABLES:
            raise ValueError('Invalid link-node variable specified: "{}". Must be one of: "{}"'.format(
                variable,
                '", "'.join(self.VALID_LINK_NODE_VARIABLES)
            ))

        # Get Layer Name
        layer_name = self.get_unique_item_name(item_name=self.VL_LINK_NODE, suffix=variable, model_db=model_db)

        # Get Default Style Name
        default_style = self.get_unique_item_name(self.VL_LINK_NODE, variable=variable)

        # Render SQL
        sql_template_file = os.path.join(self.SQL_PATH, self.VL_LINK_NODE + '.sql')

        sql_context = {
            'variable': variable
        }

        with open(sql_template_file, 'r') as sql_template_file:
            text = sql_template_file.read()
            template = Template(text)
            sql = ' '.join(template.render(sql_context).split())

        # Create SQL View
        self.gs_engine.create_sql_view_layer(
            store_id=f"{self.WORKSPACE}:{model_db.get_id()}",
            layer_name=layer_name,
            geometry_type=self.GT_POINT,
            srid=srid,
            sql=sql,
            default_style=default_style,
            parameters=(
                {
                    'name': 'scenarioid',
                    'default_value': '1',
                    'regex_validator': '^[0-9]+$'
                },
                {
                    'name': 'timesummary',
                    'default_value': 'Avg',
                    'regex_validator': '^[A-Za-z]+$'
                }
            )
        )

    @reload_config()
    def delete_link_node_dataset_layer(self, model_db, variable, recurse=True, reload_config=True):
        """
        Delete a link-node dataset for the given variable.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            variable(str): the link node dataset variable. One of GsshaSpatialManager.LN_STREAM_FLOW or GsshaSpatialManager.LN_STREAM_DEPTH.
            recurse(bool): recursively delete any dependent GeoServer objects if True.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """  # noqa: E501
        if variable not in self.VALID_LINK_NODE_VARIABLES:
            raise ValueError('Invalid link-node variable specified: "{}". Must be one of: "{}"'.format(
                variable,
                '", "'.join(self.VALID_LINK_NODE_VARIABLES)
            ))

        layer_name = self.get_unique_item_name(item_name=self.VL_LINK_NODE, suffix=variable, model_db=model_db)
        self.gs_engine.delete_layer(
            layer_id=f"{self.WORKSPACE}:{layer_name}",
            datastore=model_db.get_id(),
            recurse=recurse
        )

    @reload_config()
    def create_raster_layer(self, model_db, raster_layer_type, scenario_id=BASE_SCENARIO_ID, srid=3857,
                            raster_map_file=None, default_style='', other_styles=None, reload_config=True):
        """
        Create a raster layer for GSSHA models rasters.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            raster_layer_type(str): the type of the raster layer to create (one of RL_ELEVATION, RL_MASK, RL_INDEX).
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            raster_map_file(str): Path to the GSSHA raster file (e.g.: *.ele, *.msk, and *.idx).
            default_style (str): The name of the default style (note: it is assumed this style belongs to the workspace).
            other_styles (list): A list of other default style names (assumption: these styles belong to the workspace).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """  # noqa: E501
        # Get Coverage Name
        if raster_layer_type == self.RL_INDEX:
            raster_file_name = os.path.basename(raster_map_file)
            raster_map_id = raster_file_name.split('.')[0]
            coverage_name = self.get_unique_item_name(item_name=raster_layer_type, suffix=raster_map_id,
                                                      model_db=model_db, scenario_id=scenario_id)
        else:
            coverage_name = self.get_unique_item_name(item_name=raster_layer_type, model_db=model_db,
                                                      scenario_id=scenario_id)

        # Get the WKT Projection of the srid
        projection_string = self.get_projection_string(model_db=model_db, srid=srid)

        # create projection file in temp
        _, tmp_prj_path = tempfile.mkstemp(suffix='.prj')

        with open(tmp_prj_path, 'w') as tmp_prj_file:
            tmp_prj_file.write(projection_string)

        # zip raster file and projection file together
        _, tmp_zip_path = tempfile.mkstemp(suffix='.zip')

        with zipfile.ZipFile(tmp_zip_path, 'w') as tmp_zip_file:
            # NOTE: Give project file and raster file same basename when zipping
            tmp_zip_file.write(tmp_prj_path, coverage_name + '.prj')
            tmp_zip_file.write(raster_map_file, coverage_name)

        self.gs_engine.create_coverage_layer(
            layer_id=f"{self.WORKSPACE}:{coverage_name}",
            coverage_type=self.gs_engine.CT_GRASS_GRID,
            coverage_file=tmp_zip_path,
            default_style=default_style,
            other_styles=other_styles
        )

    @reload_config()
    def delete_raster_layer(self, model_db, raster_layer_type, scenario_id=BASE_SCENARIO_ID, index_raster_id=None,
                            reload_config=True):
        """
        Delete raster layer and all associated GeoServer objects (resource and store).
        Args:
            model_db(ModelDatabase): the object representing the models database.
            raster_layer_type(str): the type of the raster layer to create (one of RL_ELEVATION, RL_MASK, RL_INDEX).
            index_raster_id(str): identifier for index raster map. Required for RL_INDEX raster layers.

        """
        # Get the store name
        if raster_layer_type == self.RL_INDEX and index_raster_id is None:
            raise ValueError('Must provide "index_raster_id" parameter for RL_INDEX layers.')

        if raster_layer_type != self.RL_INDEX:
            coverage_store_name = self.get_unique_item_name(item_name=raster_layer_type, model_db=model_db,
                                                            scenario_id=scenario_id)
        else:
            coverage_store_name = self.get_unique_item_name(item_name=raster_layer_type, suffix=index_raster_id,
                                                            model_db=model_db, scenario_id=scenario_id)

        self.gs_engine.delete_coverage_store(
            store_id=f"{self.WORKSPACE}:{coverage_store_name}",
            recurse=True,
            purge=True
        )

    @reload_config()
    def create_elevation_raster_layer(self, model_db, srid, raster_map_file, scenario_id=BASE_SCENARIO_ID,
                                      reload_config=True):
        """
        Create an elevation raster layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            raster_map_file(str): Path to the GSSHA elevation raster file (i.e.: *.ele).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        self.create_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_ELEVATION,
            srid=srid,
            raster_map_file=raster_map_file,
            default_style=self.get_unique_item_name(self.RL_ELEVATION),
            reload_config=False
        )

    @reload_config()
    def delete_elevation_raster_layer(self, model_db, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        Delete the elevation raster.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True

        """
        self.delete_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_ELEVATION,
            reload_config=False
        )

    @reload_config()
    def create_mask_raster_layer(self, model_db, srid, raster_map_file, scenario_id=BASE_SCENARIO_ID,
                                 reload_config=True):
        """
        Create an mask raster layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            raster_map_file(str): Path to the GSSHA mask raster file (i.e.: *.msk).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        self.create_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_MASK,
            srid=srid,
            raster_map_file=raster_map_file,
            default_style=self.get_unique_item_name(self.RL_MASK),
            reload_config=False
        )

    @reload_config()
    def delete_mask_raster_layer(self, model_db, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        Delete the mask raster.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True

        """
        self.delete_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_MASK,
            reload_config=False
        )

    @reload_config()
    def create_index_map_raster_layer(self, model_db, srid, raster_map_file, scenario_id=BASE_SCENARIO_ID,
                                      reload_config=True):
        """
        Create an index raster layer.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            raster_map_file(str): Path to the GSSHA index raster file (i.e.: *.idx).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        self.create_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_INDEX,
            srid=srid,
            raster_map_file=raster_map_file,
            default_style=self.get_unique_item_name(self.RL_INDEX),
            reload_config=False
        )

    @reload_config()
    def delete_index_map_raster_layer(self, model_db, index_map_id, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        Delete the mask raster.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            index_map_id(str): the id/name of the index map.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        self.delete_raster_layer(
            model_db=model_db,
            scenario_id=scenario_id,
            raster_layer_type=self.RL_INDEX,
            index_raster_id=index_map_id,
            reload_config=False
        )

    @reload_config()
    def create_all_index_map_raster_layers(self, model_db, srid, raster_map_files, scenario_id=BASE_SCENARIO_ID,
                                           reload_config=True):
        """
        Create all index map raster layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            srid(int): EPSG Spatial Reference ID. Defaults to Mercator, 3857.
            raster_map_files(list<str>): List of paths to the GSSHA index raster files (i.e.: *.idx).
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        for raster_map_file in raster_map_files:
            self.create_index_map_raster_layer(
                model_db=model_db,
                scenario_id=scenario_id,
                srid=srid,
                raster_map_file=raster_map_file,
                reload_config=False
            )

    @reload_config()
    def delete_all_index_map_raster_layers(self, model_db, scenario_id=BASE_SCENARIO_ID, reload_config=True):
        """
        Delete all of the index map raster layers.

        Args:
            model_db(ModelDatabase): the object representing the models database.
            scenario_id(int): id of the scenario.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True
        """
        # Get list of index map rasters from db
        index_map_ids = []
        sql = f"""SELECT idx_index_maps.filename FROM idx_index_maps
                  JOIN prj_project_files ON idx_index_maps."mapTableFileID" = prj_project_files."mapTableFileID"
                  WHERE prj_project_files.id = {scenario_id};"""

        db_engine = model_db.get_engine()
        try:
            rows = db_engine.execute(sql)

            for row in rows:
                file_name = row.filename.split('.')
                index_map_ids.append(file_name[0])
        finally:
            db_engine.dispose()

        for index_map_id in index_map_ids:
            self.delete_index_map_raster_layer(
                model_db=model_db,
                scenario_id=scenario_id,
                index_map_id=index_map_id,
                reload_config=False
            )

    @reload_config()
    def create_model_boundary_styles(self, overwrite=False, reload_config=True):
        """
        Create styles for models boundary layers.
        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Create Base Style
        context = {}
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_MODEL_BOUNDARY)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_MODEL_BOUNDARY + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

        # Create Labels Style
        context = {
            'is_label_style': True,
            'label_property': 'area'
        }
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_MODEL_BOUNDARY, suffix=self.LABELS_SUFFIX)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_MODEL_BOUNDARY + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_model_boundary_styles(self, purge=True, reload_config=True):
        """
        Delete models boundary styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_MODEL_BOUNDARY)}",
            purge=purge
        )

        # Delete Labels Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_MODEL_BOUNDARY, suffix=self.LABELS_SUFFIX)}",
            purge=purge
        )

    @reload_config()
    def create_stream_links_styles(self, overwrite=False, reload_config=True):
        """
        Create styles for stream links layers.
        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Create Base Style
        context = {}
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_LINKS)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_STREAM_LINKS + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

        # Create Labels Style
        context = {
            'is_label_style': True,
            'label_property': 'linkNumber'
        }
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_LINKS, suffix=self.LABELS_SUFFIX)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_STREAM_LINKS + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_stream_links_styles(self, purge=True, reload_config=True):
        """
        Delete stream links styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_LINKS)}",
            purge=purge
        )

        # Delete Labels Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_LINKS, suffix=self.LABELS_SUFFIX)}",
            purge=purge
        )

    @reload_config()
    def create_stream_nodes_styles(self, overwrite=False, reload_config=True):
        """
        Create styles for stream nodes layers.
        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Create Base Style
        context = {}
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_NODES)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_STREAM_NODES + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

        # Create Labels Style
        context = {
            'is_label_style': True,
            'label_property': 'nodeNumber'
        }
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_NODES, suffix=self.LABELS_SUFFIX)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_STREAM_NODES + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_stream_nodes_styles(self, purge=True, reload_config=True):
        """
        Delete stream nodes styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_NODES)}",
            purge=purge
        )

        # Delete Labels Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_STREAM_NODES, suffix=self.LABELS_SUFFIX)}",
            purge=purge
        )

    @reload_config()
    def create_link_node_dataset_styles(self, variable, overwrite=False, reload_config=True):
        """
        Create styles for link-node dataset layers.
        Args:
            variable(str): the link node dataset variable. One of GsshaSpatialManager.LN_STREAM_FLOW or GsshaSpatialManager.LN_STREAM_DEPTH.
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """  # noqa: E501
        if variable not in self.VALID_LINK_NODE_VARIABLES:
            raise ValueError('Invalid link-node variable specified: "{}". Must be one of: "{}"'.format(
                variable,
                '", "'.join(self.VALID_LINK_NODE_VARIABLES)
            ))

        # Create Base Style
        context = self.LN_DEFAULT_DIVISIONS[variable]
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_LINK_NODE, variable=variable)}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_LINK_NODE + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

        # Create Labels Style
        context = {
            'is_label_style': True,
            'label_property': 'value'
        }
        context.update(self.LN_DEFAULT_DIVISIONS[variable])

        style_name = self.get_unique_item_name(self.VL_LINK_NODE, variable=variable, suffix=self.LABELS_SUFFIX)
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{style_name}",
            sld_template=os.path.join(self.SLD_PATH, self.VL_LINK_NODE + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_link_node_dataset_styles(self, variable, purge=True, reload_config=True):
        """
        Delete link-node dataset styles.
        Args:
            variable(str): the link node dataset variable. One of GsshaSpatialManager.LN_STREAM_FLOW or GsshaSpatialManager.LN_STREAM_DEPTH.
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """  # noqa: E501
        if variable not in self.VALID_LINK_NODE_VARIABLES:
            raise ValueError('Invalid link-node variable specified: "{}". Must be one of: "{}"'.format(
                variable,
                '", "'.join(self.VALID_LINK_NODE_VARIABLES)
            ))

        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.VL_LINK_NODE, variable=variable)}",
            purge=purge
        )

        # Delete Labels Style
        style_name = self.get_unique_item_name(self.VL_LINK_NODE, variable=variable, suffix=self.LABELS_SUFFIX)
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{style_name}",
            purge=purge
        )

    @reload_config()
    def create_elevation_raster_styles(self, overwrite=False, reload_config=True):
        """
        Create elevation raster styles.
        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Create Base Style

        context = {}
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_ELEVATION)}",
            sld_template=os.path.join(self.SLD_PATH, self.RL_ELEVATION + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_elevation_raster_styles(self, purge=True, reload_config=True):
        """
        Delete elevation raster styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_ELEVATION)}",
            purge=purge
        )

    @reload_config()
    def create_mask_raster_styles(self, overwrite=False, reload_config=True):
        """
        Create mask_raster_styles.
        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Create Base Style
        context = {
            'active_color': '#000000'
        }
        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_MASK)}",
            sld_template=os.path.join(self.SLD_PATH, self.RL_MASK + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_mask_raster_styles(self, purge=True, reload_config=True):
        """
        Delete mask raster styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_MASK)}",
            purge=purge
        )

    @reload_config()
    def create_index_map_raster_styles(self, overwrite=False, reload_config=True):
        """
        Create_index_map_raster_styles

        Args:
            overwrite(bool): Overwrite style if already exists when True. Defaults to False.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        context = {}

        self.gs_engine.create_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_INDEX)}",
            sld_template=os.path.join(self.SLD_PATH, self.RL_INDEX + '.sld'),
            sld_context=context,
            overwrite=overwrite
        )

    @reload_config()
    def delete_index_map_raster_styles(self, purge=True, reload_config=True):
        """
        Delete index map raster styles.
        Args:
            purge(bool): Force remove all resources associated with style.
            reload_config(bool): Reload the GeoServer node configuration and catalog before returning if True.
        """
        # Delete Base Style
        self.gs_engine.delete_style(
            style_id=f"{self.WORKSPACE}:{self.get_unique_item_name(self.RL_INDEX)}",
            purge=purge
        )