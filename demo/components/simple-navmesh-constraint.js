/**
 * simple-navmesh-constraint
 * Prevents the camera rig from walking through walls and large furniture.
 * Uses AABB (axis-aligned bounding box) checks against elements with class="collidable".
 */
AFRAME.registerComponent('simple-navmesh-constraint', {
  schema: {
    enabled:  { type: 'boolean', default: true },
    minX:     { type: 'number',  default: -9.5 },
    maxX:     { type: 'number',  default:  9.5 },
    minZ:     { type: 'number',  default: -15.5 },
    maxZ:     { type: 'number',  default:  11.5 },
    margin:   { type: 'number',  default:  0.3 }
  },

  init: function () {
    this.obstacles = [];
    this._camChild = this.el.querySelector('[camera]') || null;
    this._gatherObstacles();

    // Re-gather when scene loads fully (in case entities load late)
    var self = this;
    this.el.sceneEl.addEventListener('loaded', function () {
      self._gatherObstacles();
      if (!self._camChild) {
        self._camChild = self.el.querySelector('[camera]');
      }
    });
  },

  _gatherObstacles: function () {
    this.obstacles = [];
    var els = this.el.sceneEl.querySelectorAll('.collidable');
    for (var i = 0; i < els.length; i++) {
      var ob = this._extractAABB(els[i]);
      if (ob) this.obstacles.push(ob);
    }
  },

  _extractAABB: function (el) {
    var pos = el.getAttribute('position');
    if (!pos) return null;

    var w = 0, d = 0;
    var geom = el.getAttribute('geometry');
    var rot = el.getAttribute('rotation');
    var rotY = rot ? rot.y : 0;

    // Handle a-plane / a-box / a-cylinder
    if (geom) {
      if (geom.primitive === 'plane' || geom.primitive === 'box') {
        w = geom.width || 1;
        d = geom.depth || geom.height || 0.1;
      } else if (geom.primitive === 'cylinder') {
        w = (geom.radius || 0.5) * 2;
        d = w;
      }
    }

    // Fallback to element attributes
    if (w === 0) {
      w = parseFloat(el.getAttribute('width')) || 1;
      d = parseFloat(el.getAttribute('depth')) || 0.1;
    }

    // If rotated 90 degrees, swap width and depth
    if (Math.abs(rotY % 180) > 45 && Math.abs(rotY % 180) < 135) {
      var tmp = w; w = d; d = tmp;
    }

    var m = this.data.margin;
    return {
      minX: pos.x - w / 2 - m,
      maxX: pos.x + w / 2 + m,
      minZ: pos.z - d / 2 - m,
      maxZ: pos.z + d / 2 + m
    };
  },

  tick: function () {
    if (!this.data.enabled) return;

    var pos = this.el.object3D.position;
    var d = this.data;

    // Account for camera child offset (wasd-controls moves camera, not rig)
    var cx = 0, cz = 0;
    if (this._camChild) {
      cx = this._camChild.object3D.position.x;
      cz = this._camChild.object3D.position.z;
    }

    // Effective player position (rig + camera offset)
    var ex = pos.x + cx;
    var ez = pos.z + cz;

    // Clamp to room bounds
    if (ex < d.minX) pos.x = d.minX - cx;
    if (ex > d.maxX) pos.x = d.maxX - cx;
    if (ez < d.minZ) pos.z = d.minZ - cz;
    if (ez > d.maxZ) pos.z = d.maxZ - cz;

    // Recalculate after clamp
    ex = pos.x + cx;
    ez = pos.z + cz;

    // Resolve obstacle overlaps (push out along axis of least penetration)
    for (var i = 0; i < this.obstacles.length; i++) {
      var ob = this.obstacles[i];
      if (ex > ob.minX && ex < ob.maxX && ez > ob.minZ && ez < ob.maxZ) {
        var pushLeft  = ex - ob.minX;
        var pushRight = ob.maxX - ex;
        var pushBack  = ez - ob.minZ;
        var pushFront = ob.maxZ - ez;
        var minPush = Math.min(pushLeft, pushRight, pushBack, pushFront);

        if (minPush === pushLeft)       pos.x = ob.minX - cx;
        else if (minPush === pushRight) pos.x = ob.maxX - cx;
        else if (minPush === pushBack)  pos.z = ob.minZ - cz;
        else                            pos.z = ob.maxZ - cz;

        ex = pos.x + cx;
        ez = pos.z + cz;
      }
    }
  }
});
