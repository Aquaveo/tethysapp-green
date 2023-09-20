from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import Button, CesiumMapView, MVLayer

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    cesium_ion_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3ZTJiMWRlNy0zODQ4LTRiZjItYjc2Ni0zNmQzMTQ1NzRlMWUiLCJpZCI6MjE3MzAsImlhdCI6MTY5NTE2NDQ1M30.eXHTikmSsCH5rYpG2O_Ii0qb5Vdpu2fOV8S82YDptTM'
    
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