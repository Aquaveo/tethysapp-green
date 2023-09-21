from tethysext.atcore.controllers.map_view import MapView
from tethysapp.green.app import Green as app


class GreenMapView(MapView):
    """Controller for the map view page."""
    map_title = 'GREEN Map'
    map_subtitle = 'GSSHA Models'
    map_type = 'cesium_map_view'
    base_template = 'green/base.html'
    template_name = 'green/home_map_view.html'

    def default_back_url(self, request, *args, **kwargs):
        """
        Hook for custom back url. Defaults to the resource details page.
        Returns:
            str: back url.
        """
        return 'green:home'

    def get_sessionmaker(self):
        return app.get_persistent_store_database(
            app.DATABASE_NAME,
            as_sessionmaker=True
        )
