/**
 * click-to-move
 * Click on the floor (.walkable) to move the camera rig to that point.
 * Works alongside WASD controls. Pressing any WASD key cancels the move.
 * Respects simple-navmesh-constraint automatically (constraint runs after).
 */
AFRAME.registerComponent('click-to-move', {
  schema: {
    speed:       { type: 'number', default: 4 },
    arrivalDist: { type: 'number', default: 0.3 }
  },

  init: function () {
    this.target = null;
    this.moving = false;
    this.marker = null;
    this._direction = new THREE.Vector3();

    this._createMarker();
    this._bindEvents();
  },

  _createMarker: function () {
    this.marker = document.createElement('a-ring');
    this.marker.setAttribute('radius-inner', 0.15);
    this.marker.setAttribute('radius-outer', 0.25);
    this.marker.setAttribute('color', '#4DD0E1');
    this.marker.setAttribute('rotation', '-90 0 0');
    this.marker.setAttribute('position', '0 0.03 0');
    this.marker.setAttribute('material', 'opacity: 0.7; transparent: true');
    this.marker.setAttribute('visible', false);
    this.marker.setAttribute('id', 'move-marker');
    this.el.sceneEl.appendChild(this.marker);
  },

  _bindEvents: function () {
    var self = this;

    // Listen for clicks on walkable surfaces
    this.el.sceneEl.addEventListener('loaded', function () {
      var walkables = self.el.sceneEl.querySelectorAll('.walkable');
      for (var i = 0; i < walkables.length; i++) {
        walkables[i].addEventListener('click', function (evt) {
          if (evt.detail && evt.detail.intersection) {
            self._setTarget(evt.detail.intersection.point);
          }
        });
      }
    });

    // Cancel on WASD
    document.addEventListener('keydown', function (evt) {
      var key = evt.key.toLowerCase();
      if (key === 'w' || key === 'a' || key === 's' || key === 'd' ||
          key === 'arrowup' || key === 'arrowdown' || key === 'arrowleft' || key === 'arrowright') {
        self._cancel();
      }
    });
  },

  _setTarget: function (point) {
    this.target = new THREE.Vector3(point.x, 0, point.z);
    this.moving = true;

    // Show marker at target
    this.marker.setAttribute('position', point.x + ' 0.03 ' + point.z);
    this.marker.setAttribute('visible', true);

    // Pulse animation on marker
    this.marker.removeAttribute('animation');
    this.marker.setAttribute('animation', {
      property: 'material.opacity',
      from: 0.9,
      to: 0.2,
      dur: 800,
      easing: 'easeInQuad',
      loop: true,
      dir: 'alternate'
    });
  },

  _cancel: function () {
    this.moving = false;
    this.target = null;
    if (this.marker) this.marker.setAttribute('visible', false);
  },

  tick: function (time, delta) {
    if (!this.moving || !this.target) return;

    var rig = this.el.object3D.position;
    var dt = delta / 1000;

    // Direction to target (XZ only)
    this._direction.set(
      this.target.x - rig.x,
      0,
      this.target.z - rig.z
    );

    var dist = this._direction.length();
    if (dist < this.data.arrivalDist) {
      this._cancel();
      return;
    }

    this._direction.normalize();
    var step = this.data.speed * dt;
    if (step > dist) step = dist;

    rig.x += this._direction.x * step;
    rig.z += this._direction.z * step;
  }
});
