import logging
from tethysext.atcore.controllers.resources import TabbedResourceDetails

from tethysapp.green.controllers.gssha_models.tabs.gssha_model_summary_tab import GsshaModelSummaryTab
from tethysapp.green.controllers.gssha_models.tabs.gssha_model_workflows_tab import GsshaModelWorkflowsTab


log = logging.getLogger('tethys.' + __name__)


class GsshaModelDetails(TabbedResourceDetails):
    """
    Controller for gssha model details page(s).
    """
    base_template = 'green/base.html'
    tabs = (
        {'slug': 'summary', 'title': 'Summary', 'view': GsshaModelSummaryTab},
        {'slug': 'workflows', 'title': 'Workflows', 'view': GsshaModelWorkflowsTab},
    )
