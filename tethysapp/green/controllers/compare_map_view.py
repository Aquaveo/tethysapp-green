import json

from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import CesiumMapView, MVLayer
from tethysapp.green.app import Green as app


@login_required()
def compare(request):
    """
    Controller for the app home page.
    """
    cesium_ion_token = app.get_custom_setting('cesium_api_key')


    # Hacky Cesium stuff
    # to use within the javascript to load the Cesium library

    # watershed = MVLayer(
    #     source='ImageWMS',
    #     legend_title='Park City',
    #     options={
    #         'url': 'http://localhost:8181/geoserver/wms',
    #         'params': {'LAYERS': 'gssha:gssha_model'},
    #         'serverType': 'geoserver'
    #     },
    # )

    terrain_provider = {
        'Cesium.createWorldTerrain': {
            'requestVertexNormals': True,
            'requestWaterMask': True
        }
    }

    cesium_map_view = CesiumMapView(
        cesium_ion_token=cesium_ion_token,
        layers=[],
        terrain={'terrainProvider': terrain_provider},
    )

    # end of hacky cesium stuff
    
    from tethysext.atcore.models.app_users import AppUser
    from tethysext.atcore.services.model_database import ModelDatabase
    from tethysapp.green.models import GsshaModel

    gs_engine = app.get_spatial_dataset_service(
                    name=app.GEOSERVER_NAME,
                    as_engine=True
                )
    endpoint = gs_engine.endpoint.replace('/rest/', '')
    

    session = app.get_persistent_store_database(app.DATABASE_NAME, as_sessionmaker=True)()

    dropdownList = []

    try:
        request_app_user = AppUser.get_app_user_from_request(request, session)
        
        gssha_models = request_app_user.get_resources(
            session=session,
            request=request,
            of_type=GsshaModel,
        )

        for model in gssha_models:
            print(model.get_attribute('database_id'))
            db_id = model.get_attribute('database_id').replace("_", "-")
            dropdownList.append([model.name, db_id])

    finally:
        session.close()

    

    context = {
        'cesium_map_view': cesium_map_view,
        'cesium_ion_token': cesium_ion_token,
        'ddl': dropdownList,
        'gs_endpoint': endpoint,
    }

    return render(request, 'green/compare.html', context)
