/**
 * Proximity Panel Component
 * Shows/hides an info panel when the camera comes within range.
 */
AFRAME.registerComponent('proximity-panel', {
  schema: {
    target: { type: 'selector' },
    range: { type: 'number', default: 4 },
    camRig: { type: 'selector', default: '[camera]' }
  },

  init: function () {
    this.panelVisible = false;
    this._hideTimer = null;
    this._rigPos = new THREE.Vector3();
    this._myPos = new THREE.Vector3();

    if (this.data.target) {
      this.data.target.setAttribute('visible', false);
      this.data.target.setAttribute('scale', '0.01 0.01 0.01');
    }

    this.tick = AFRAME.utils.throttleTick(this.tick, 150, this);
  },

  tick: function () {
    if (!this.data.target || !this.data.camRig) return;

    this.data.camRig.object3D.getWorldPosition(this._rigPos);
    this.el.object3D.getWorldPosition(this._myPos);

    // Check XZ distance only
    var dx = this._rigPos.x - this._myPos.x;
    var dz = this._rigPos.z - this._myPos.z;
    var dist = Math.sqrt(dx * dx + dz * dz);
    var inRange = dist < this.data.range;

    if (inRange && !this.panelVisible) {
      if (this._hideTimer) { clearTimeout(this._hideTimer); this._hideTimer = null; }
      this.data.target.setAttribute('visible', true);
      this.data.target.removeAttribute('animation');
      this.data.target.setAttribute('animation', {
        property: 'scale',
        from: '0.01 0.01 0.01',
        to: '1 1 1',
        dur: 300,
        easing: 'easeOutQuad'
      });
      this.panelVisible = true;
    } else if (!inRange && this.panelVisible) {
      this.data.target.removeAttribute('animation');
      this.data.target.setAttribute('animation', {
        property: 'scale',
        from: '1 1 1',
        to: '0.01 0.01 0.01',
        dur: 200,
        easing: 'easeInQuad'
      });
      var target = this.data.target;
      this._hideTimer = setTimeout(function () {
        target.setAttribute('visible', false);
      }, 250);
      this.panelVisible = false;
    }

  }
});
