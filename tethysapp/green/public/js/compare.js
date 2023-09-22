$(function() {
  // We want our two views to be synced across time, so we create
  // a shared clock object that both views share
  var token = document.getElementById('cesium_ion_token').innerText;
  var gs_endpoint = document.getElementById('gs_endpoint').innerText;
  Cesium.Ion.defaultAccessToken = token;
  document.getElementById('cesium_ion_token').remove();

  console.log(gs_endpoint);

  const clockViewModel = new Cesium.ClockViewModel();
  const options3D = {
    fullscreenButton: false,
    sceneModePicker: false,
    clockViewModel: clockViewModel,
    terrainProvider : Cesium.createWorldTerrain(),
  };

  // We create two viewers, a 2D and a 3D one
  // The CSS is set up to place them side by side
  const view3DL = new Cesium.Viewer("view3DL", options3D);
  const view3DR = new Cesium.Viewer("view3DR", options3D);

  function syncLViewDumb() {
    view3DR.scene.camera = view3DL.scene.camera;
  }

  function syncRViewDumb() {
    view3DL.scene.camera = view3DR.scene.camera;
  }

  // Apply our sync function every time the 3D camera view changes
  view3DL.camera.changed.addEventListener(syncLViewDumb);
  view3DR.camera.changed.addEventListener(syncRViewDumb);
  // By default, the `camera.changed` event will trigger when the camera has changed by 50%
  // To make it more sensitive, we can bring down this sensitivity
  view3DL.camera.percentageChanged = 0.1;

  // select default options
  var selectL = document.getElementById('selectL');
  var selectR = document.getElementById('selectR');

  // if there's 2 or more options in the selector,
  //   have the left one select the first one
  //   and have the right one select the second
  if (selectL.length >= 2) {
    selectL.value = selectL[0].value;
    selectR.value = selectR[1].value;
  }

  //initialise WMS provider
  const WMSparameters = {
    version: '1.3.0',
    format: 'image/png',
    srs: 'EPSG:4326',
    transparent: true,
    // "exceptions": 'application/vnd.ogc.se_inimage',
  };

  // TODO: make a selector for the background raster
  //       currently 1_index_Combined

  var elevationL = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectL.value}_1_index_Combined`,
    parameters: WMSparameters,
  });
  var boundaryL = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectL.value}_model_boundary`,
    parameters: WMSparameters,
  });
  var streamsL = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectL.value}_stream_links`,
    parameters: WMSparameters,
  });

  var elevationR = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectR.value}_1_index_Combined`,
    parameters: WMSparameters,
  });
  var boundaryR = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectR.value}_model_boundary`,
    parameters: WMSparameters,
  });
  var streamsR = new Cesium.WebMapServiceImageryProvider({
    url : `${gs_endpoint}/wms`,
    layers : `green:${selectR.value}_stream_links`,
    parameters: WMSparameters,
  });

  view3DL.imageryLayers.addImageryProvider(elevationL);
  view3DL.imageryLayers.addImageryProvider(boundaryL);
  view3DL.imageryLayers.addImageryProvider(streamsL);

  view3DR.imageryLayers.addImageryProvider(elevationR);
  view3DR.imageryLayers.addImageryProvider(boundaryR);
  view3DR.imageryLayers.addImageryProvider(streamsR);

  selectL.addEventListener('change', function() {
    let layers = [];
    for (let i = 1; i < view3DL.imageryLayers.length; i++) {
      layers.push(view3DL.imageryLayers.get(i))
    }
    for (let i = 0; i < layers.length; i++) {
      view3DL.imageryLayers.remove(layers[i])
    }

    elevationL = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectL.value}_1_index_Combined`,
      parameters: WMSparameters,
    });
    boundaryL = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectL.value}_model_boundary`,
      parameters: WMSparameters,
    });
    streamsL = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectL.value}_stream_links`,
      parameters: WMSparameters,
    });

    view3DL.imageryLayers.addImageryProvider(elevationL);
    view3DL.imageryLayers.addImageryProvider(boundaryL);
    view3DL.imageryLayers.addImageryProvider(streamsL);
  })

  selectR.addEventListener('change', function() {
    let layers = [];
    for (let i = 1; i < view3DR.imageryLayers.length; i++) {
      layers.push(view3DR.imageryLayers.get(i))
    }
    for (let i = 0; i < layers.length; i++) {
      view3DR.imageryLayers.remove(layers[i])
    }

    console.log(view3DR.imageryLayers);

    elevationR = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectR.value}_1_index_Combined`,
      parameters: WMSparameters,
    });
    boundaryR = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectR.value}_model_boundary`,
      parameters: WMSparameters,
    });
    streamsR = new Cesium.WebMapServiceImageryProvider({
      url : `${gs_endpoint}/wms`,
      layers : `green:${selectR.value}_stream_links`,
      parameters: WMSparameters,
    });

    view3DR.imageryLayers.addImageryProvider(elevationR);
    view3DR.imageryLayers.addImageryProvider(boundaryR);
    view3DR.imageryLayers.addImageryProvider(streamsR);
  })


});