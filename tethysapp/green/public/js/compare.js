$(function() {
  // We want our two views to be synced across time, so we create
  // a shared clock object that both views share
  var token = document.getElementById('cesium_ion_token').innerText;
  console.log(document.getElementById('cesium_ion_token'));
  console.log(token);
  Cesium.Ion.defaultAccessToken = token;
  // document.getElementById('cesium_ion_token').remove();

  const clockViewModel = new Cesium.ClockViewModel();
  const options3D = {
    fullscreenButton: false,
    sceneModePicker: false,
    clockViewModel: clockViewModel,
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
});