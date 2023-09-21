import argparse
from tethys_dataset_services.engines import GeoServerSpatialDatasetEngine
from tethysext.atcore.utilities import parse_url
from tethysapp.green.services.spatial_manager import GsshaSpatialManager


def init_green(arguments):
    """
    Commandline interface for initializing the green app.
    """
    errors_occurred = False
    print('Initializing GREEN...')

    url = parse_url(arguments.gsurl)

    geoserver_engine = GeoServerSpatialDatasetEngine(
        endpoint=url.endpoint,
        username=url.username,
        password=url.password
    )

    gsm = GsshaSpatialManager(
        geoserver_engine=geoserver_engine
    )

    # Initialize workspace
    print('Initializing GREEN GeoServer Workspace...')
    try:
        gsm.create_workspace()
        print('Successfully initialized GREEN GeoServer workspace.')
    except Exception as e:
        errors_occurred = True
        print('An error occurred during workspace creation: {}'.format(e))

    # Initialize styles
    print('Initializing GREEN GeoServer Styles...')
    try:
        gsm.create_all_styles(overwrite=True)
        print('Successfully initialized GREEN GeoServer styles.')
    except Exception as e:
        errors_occurred = True
        print('An error occurred during style creation: {}'.format(e))

    if not errors_occurred:
        print('Successfully initialized GREEN.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'gsurl',
        help='GeoServer url to geoserver rest endpoint '
             '(e.g.: "http://admin:geoserver@localhost:8181/geoserver/rest/").'
    )
    parser.set_defaults(func=init_green)
    args = parser.parse_args()
    args.func(args)