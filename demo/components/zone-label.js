/**
 * Zone Label Component
 * Creates a floating text label above a zone that always faces the camera.
 */
AFRAME.registerComponent('zone-label', {
  schema: {
    text: { type: 'string', default: 'ZONA' },
    color: { type: 'color', default: '#FFFFFF' },
    width: { type: 'number', default: 8 },
    yOffset: { type: 'number', default: 2.8 }
  },

  init: function () {
    this._camPos = new THREE.Vector3();
    this._labelPos = new THREE.Vector3();

    var container = document.createElement('a-entity');
    container.setAttribute('position', '0 ' + this.data.yOffset + ' 0');

    // Background plane
    var bg = document.createElement('a-plane');
    bg.setAttribute('width', this.data.text.length * 0.22 + 0.6);
    bg.setAttribute('height', 0.45);
    bg.setAttribute('color', this.data.color);
    bg.setAttribute('material', 'opacity: 0.2; transparent: true; side: double');

    // Text
    var label = document.createElement('a-entity');
    label.setAttribute('text', {
      value: this.data.text,
      color: this.data.color,
      align: 'center',
      width: this.data.width,
      font: 'roboto',
      anchor: 'center'
    });
    label.setAttribute('position', '0 0 0.02');

    container.appendChild(bg);
    container.appendChild(label);
    this.el.appendChild(container);
    this.container = container;
  },

  tick: function () {
    var camera = this.el.sceneEl.camera;
    if (!camera || !this.container) return;

    camera.el.object3D.getWorldPosition(this._camPos);
    this.container.object3D.getWorldPosition(this._labelPos);
    this._camPos.y = this._labelPos.y;
    this.container.object3D.lookAt(this._camPos);
  }
});
