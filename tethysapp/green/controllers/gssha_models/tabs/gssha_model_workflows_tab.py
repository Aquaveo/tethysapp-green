from tethysext.atcore.controllers.resources import ResourceWorkflowsTab
from tethysapp.green.services.spatial_manager import GsshaSpatialManager
from tethysapp.green.services.map_manager import GreenMapManager


GSSHA_WORKFLOWS = []


class GsshaModelWorkflowsTab(ResourceWorkflowsTab):

    @classmethod
    def get_workflow_types(cls):
        return GSSHA_WORKFLOWS

    def get_map_manager(self):
        return GreenMapManager

    def get_spatial_manager(self):
        return GsshaSpatialManager

    def get_sds_setting_name(self):
        return self.get_app().GEOSERVER_NAME