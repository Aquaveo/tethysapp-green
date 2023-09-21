import os
import django
from django.core.exceptions import ObjectDoesNotExist


def _get_persistent_store_connection(app, name):
    """
    Custom connection getter to get connection object.
    """
    from tethys_apps.models import TethysApp
    from tethys_apps.exceptions import TethysAppSettingDoesNotExist, TethysAppSettingNotAssigned
    db_app = TethysApp.objects.get(package=app.package)
    ps_connection_settings = db_app.persistent_store_connection_settings

    try:
        # Return as_engine if the other two are False
        ps_connection_setting = ps_connection_settings.get(name=name)
        return ps_connection_setting.get_value()
    except ObjectDoesNotExist:
        raise TethysAppSettingDoesNotExist('PersistentStoreConnectionSetting', name, app.name)
    except TethysAppSettingNotAssigned:
        app._log_tethys_app_setting_not_assigned_error('PersistentStoreConnectionSetting', name)


def linkdb_command(_):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tethys_portal.settings'
    django.setup()
    from tethys_apps.utilities import create_ps_database_setting, link_service_to_app_setting
    from tethysapp.green.app import Green as app

    ps_setting_name = app.MODEL_DB_CON

    print(f'Retrieving service for setting "{ps_setting_name}"...')

    ps_conn = _get_persistent_store_connection(app, ps_setting_name)

    if not ps_conn:
        print(f'Setting "{ps_setting_name}" is required, but no service was assigned. Aborting.')
        exit(1)

    print(f'Searching for model databases for service "{ps_conn.name}"...')

    engine = ps_conn.get_engine()
    result = engine.execute(
        r"SELECT datname "
        r"FROM pg_database "
        r"WHERE datistemplate = false "
        r"AND datname SIMILAR TO 'green_\w{8}_\w{4}_\w{4}_\w{4}_\w{12}' "
        r"AND datname != 'green_primary_db';"
    )
    model_dbs = [r[0].replace('green_', '') for r in result]
    result.close()

    num_model_dbs = len(model_dbs)
    if num_model_dbs <= 0:
        print('No model databases to be linked.')
    else:
        print(f'Found {num_model_dbs} model databases.')

    for db in model_dbs:
        print(f'Creating setting for model database "{db}"...')
        create_success = create_ps_database_setting(app.package, db, initialized=True, spatial=True, dynamic=True)
        if create_success:
            print(f'Linking service "{ps_conn.name}" with new setting for model database "{db}"...')
            link_service_to_app_setting('persistent', ps_conn.name, app.package, 'ps_database', db)

    print('Successfully completed linking existing model databases.')

if __name__ == '__main__':
    linkdb_command(None)
