from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import CustomSetting, PersistentStoreDatabaseSetting, SpatialDatasetServiceSetting


class Green(TethysAppBase):
    """
    Tethys app class for GSSHA Regions for Envrionmental Engineering with Nature.
    """

    name = 'GSSHA Regions for Envrionmental Engineering with Nature'
    index = 'green:home'
    icon = 'green/images/icon.gif'
    package = 'green'
    root_url = 'green'
    color = '#77b57f'
    description = ''
    tags = ''
    enable_feedback = False
    feedback_emails = []

    DATABASE_NAME = 'primary_db'
    GEOSERVER_NAME = 'primary_geoserver'
    
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
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='green',
                controller='green.controllers.home'
            ),
        )

        return url_maps