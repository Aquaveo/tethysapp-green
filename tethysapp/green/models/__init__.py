from tethysext.atcore.models.app_users import initialize_app_users_db


def init_primary_db(engine, first_time):
    """
    Initializer for the primary database.
    """
    from .gssha_model_resource import GsshaModel  # noqa: F401
    from .green_organization import GreenOrganization  # noqa: F401
    # Initialize app users tables
    initialize_app_users_db(engine, first_time)
