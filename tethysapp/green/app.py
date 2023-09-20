from tethys_sdk.base import TethysAppBase, url_map_maker


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

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='green',
                controller='green.controllers.home'
            ),
        )

        return url_maps