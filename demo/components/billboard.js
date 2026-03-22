/**
 * Billboard Component
 * Rotates an entity to always face the camera on the Y axis.
 * Used for furniture/object planes that should face the viewer.
 */
AFRAME.registerComponent('billboard', {
  schema: {
    lockY: { type: 'boolean', default: true }
  },

  init: function () {
    this._camPos = new THREE.Vector3();
    this._entityPos = new THREE.Vector3();
  },

  tick: function () {
    var camera = this.el.sceneEl.camera;
    if (!camera) return;

    camera.el.object3D.getWorldPosition(this._camPos);
    this.el.object3D.getWorldPosition(this._entityPos);

    if (this.data.lockY) {
      this._camPos.y = this._entityPos.y;
    }

    this.el.object3D.lookAt(this._camPos);
  }
});
