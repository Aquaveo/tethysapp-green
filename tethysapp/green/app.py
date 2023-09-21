from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import (
    CustomSetting, PersistentStoreDatabaseSetting, SpatialDatasetServiceSetting, PersistentStoreConnectionSetting
)


class Green(TethysAppBase):
    """
    Tethys app class for GSSHA Regions for Envrionmental Engineering with Nature.
    """

    name = 'GSSHA Regions for Environmental Engineering with Nature'
    index = 'green:home'
    icon = 'green/images/green_250x250.png'
    package = 'green'
    root_url = 'green'
    color = '#77b57f'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    DATABASE_NAME = 'primary_db'
    GEOSERVER_NAME = 'primary_geoserver'
    MODEL_DB_CON = 'model_db_con'
    
    def custom_settings(self):
        """Custom settings."""
        custom_settings = (
            CustomSetting(
                name='cesium_api_key',
                description='API key for Cesium Ion.',
                type=CustomSetting.TYPE_STRING,
                required=False,
            ),
        )
        return custom_settings

    def persistent_store_settings(self):
        """Define Persistent Store Settings."""
        ps_settings = (
            PersistentStoreDatabaseSetting(
                name=self.DATABASE_NAME,
                description='Primary database for the Green app.',
                initializer='green.models.init_primary_db',
                required=True,
                spatial=True,
            ),
            PersistentStoreConnectionSetting(
                name=self.MODEL_DB_CON,
                description='Database connection for model dbs.',
                required=True
            ),
        )
        return ps_settings

    def spatial_dataset_service_settings(self):
        """Define spatial dataset services settings."""
        sds_settings = (
            SpatialDatasetServiceSetting(
                name=self.GEOSERVER_NAME,
                description='GeoServer used to host spatial visualizations for the app.',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True
            ),
        )
        return sds_settings

    def permissions(self):
        """Define permissions for the app."""
        from tethysext.atcore.services.app_users.permissions_manager import AppPermissionsManager
        from tethysext.atcore.permissions.app_users import PermissionsGenerator
        # Generate permissions for App Users
        pm = AppPermissionsManager(self.package)
        group = PermissionsGenerator(pm)
        permissions = group.generate()
        return permissions

    def url_maps(self):
        """Add controllers"""
        from tethysapp.green.controllers.map_view import GreenMapView
        from tethysapp.green.services.home_map_manager import HomeMapManager
        from tethysapp.green.services.spatial_manager import GsshaSpatialManager
        from tethysext.atcore.services.app_users.permissions_manager import AppPermissionsManager
        from tethysext.atcore.urls import app_users, spatial_reference
        from tethysapp.green.models import GreenOrganization, GsshaModel
        from tethysapp.green.controllers.gssha_models import (
            GsshaModelDetails, ManageGsshaModels, ModifyGsshaModel
        )

        UrlMap = url_map_maker(self.root_url)

        url_maps = []
        url_maps.append(
            UrlMap(
                name='home',
                url='green',
                controller=GreenMapView.as_controller(
                    geoserver_name=self.GEOSERVER_NAME,
                    _app=self,
                    _persistent_store_name=self.DATABASE_NAME,
                    _MapManager=HomeMapManager,
                    _Organization=GreenOrganization,
                    _Resource=GsshaModel,
                    _SpatialManager=GsshaSpatialManager,
                ),
            ),
        )

        url_maps.append(
            UrlMap(
                name='gssha_compare_resources',
                url='green/compare_resources',
                controller='green.controllers.compare_map_view.compare',
            ),
        )

        app_users_urls = app_users.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name=self.DATABASE_NAME,
            base_template='green/base.html',
            custom_models=(
                GsshaModel,
                GreenOrganization,
            ),
            custom_controllers=(
                ModifyGsshaModel,
                ManageGsshaModels
            ),
            custom_permissions_manager=AppPermissionsManager
        )
        url_maps.extend(app_users_urls)

        url_maps.extend((
            UrlMap(
                name='gssha_model_details_tab',
                url='green/gssha-models/{resource_id}/get-tab/{tab_slug}',
                controller=GsshaModelDetails.as_controller(
                    _app=self,
                    _persistent_store_name=self.DATABASE_NAME,
                    _Organization=GreenOrganization,
                    _Resource=GsshaModel,
                    _PermissionsManager=AppPermissionsManager
                ),
                regex=['[0-9A-Za-z-_.]+', '[0-9A-Za-z-_.{}]+']
            ),
        ))

        spatial_reference_urls = spatial_reference.urls(
            url_map_maker=UrlMap,
            app=self,
            persistent_store_name='primary_db'
        )
        url_maps.extend(spatial_reference_urls)

        return url_maps
