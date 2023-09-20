from django.urls import reverse

from tethysext.atcore.controllers.app_users import ManageResources


class ManageGsshaModels(ManageResources):
    def get_launch_url(self, request, resource):
        """
        Get the URL for the Resource Launch button.
        """
        return reverse('green:gssha_model_details_tab', args=[resource.id, 'summary'])

    def get_error_url(self, request, resource):
        """
        Get the URL for the Resource Launch button.
        """
        return reverse('green:gssha_model_details_tab', args=[resource.id, 'summary'])
