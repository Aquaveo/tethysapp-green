from tethysext.atcore.controllers.resources import ResourceSummaryTab
from tethysapp.green.services.map_manager import GreenMapManager
from tethysapp.green.services.spatial_manager import GsshaSpatialManager


class GsshaModelSummaryTab(ResourceSummaryTab):
    has_preview_image = True
    preview_image_title = 'Map Preview'

    def get_map_manager(self, request, resource):
        # Build spatial manager
        gs_engine = self.get_app().get_spatial_dataset_service(self.get_app().GEOSERVER_NAME, as_engine=True)
        spatial_manager = GsshaSpatialManager(geoserver_engine=gs_engine)
        return GreenMapManager(spatial_manager=spatial_manager, resource=resource)

    def get_summary_tab_info(self, request, session, resource, *args, **kwargs):
        """Define GSSHA specific summary info.

        Args:
            request (django.http.HttpRequest): the Django request object.
            session (sqlalchemy.orm.Session): the SQLAlchemy session object.
            resource (Resource): the Resource.
        """
        summary_columns = [
            [],  # Place holder for the first column, which is auto-populated with default extent and description
        ]
        summary_columns.extend([
            [
                ('General Parameters', {'key': 'value'}),
            ],
            [
                ('Output Parameters', {'key': 'value'}),
            ]
        ])
        return summary_columns

    def get_preview_image_url(self, request, resource, *args, **kwargs):
        """
        Get URL from GeoServer that will generate a PNG of the default layers.
        """
        map_manager = self.get_map_manager(request, resource)
        layer_preview_url = map_manager.get_map_preview_url()
        return layer_preview_url

    def get_watershed_area(self, resource, *args, **kwargs):
        if resource.get_attribute('area'):
            return f'{round(resource.get_attribute("area"), 2)} sq mi'