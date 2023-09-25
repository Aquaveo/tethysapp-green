from tethysext.atcore.controllers.resources import ResourceSummaryTab
from tethysapp.green.services.map_manager import GreenMapManager
from tethysapp.green.services.spatial_manager import GsshaSpatialManager


class GsshaModelSummaryTab(ResourceSummaryTab):
    has_preview_image = True
    preview_image_title = 'Map Preview'


