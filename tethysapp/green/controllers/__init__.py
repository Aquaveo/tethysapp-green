from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import CesiumMapView, MVLayer
from tethysapp.green.app import Green as app


@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    cesium_ion_token = app.get_custom_setting('cesium_api_key')
    
    watershed = MVLayer(
        source='ImageWMS',
        legend_title='Park City',
        options={
            'url': 'http://localhost:8181/geoserver/wms',
            'params': {'LAYERS': 'gssha:gssha_model'},
            'serverType': 'geoserver'
        },
    )

    terrain_provider = {
        'Cesium.createWorldTerrain': {
            'requestVertexNormals': True,
            'requestWaterMask': True
        }
    }

    cesium_map_view = CesiumMapView(
        cesium_ion_token=cesium_ion_token,
        layers=[watershed],
        terrain={'terrainProvider': terrain_provider},
    )

    context = {
        'cesium_map_view': cesium_map_view,
    }

    return render(request, 'green/home.html', context)