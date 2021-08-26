<template>
  <svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
    <rect id="box" class="bnd" :style="color" style="fill:transparent; stroke-width:1;" :x="x" :y="y" :width="w" :height="h"/>
    <rect id="box" class="bnd" style="stroke:#EBD5D2; stroke-width:1px; fill:red; fill-opacity:0.1; fill:transparent; stroke-width:1;" :x="x+0.5" :y="y" :width="w" :height="h"/>
  </svg>
</template>

<script>
export default {
  name: 'BoundingBox',
  props: ['color', 'box_info', 'border', 'circle'],
  data() {
    return {
      clicked: true,
      selected: false,
      annotated: false,
    }
  },
  computed: {
    x: function () {
      return parseInt(this.box_info.x_pos)
    },
    y: function () {
      return parseInt(this.box_info.y_pos)
    },
    w: function () {
      return parseInt(this.box_info.x_len) + 2
    },
    h: function () {
      return parseInt(this.box_info.y_len) + 2
    }
  },
  methods: {
    add: function(li) {
      var res = 0
      for (var elem in li) {
        res += this.int(li[elem])
      }
      return res
    }
  }
}
</script>
