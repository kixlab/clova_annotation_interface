<template>
  <svg width="100%" height="100%" style="position: absolute; top: 0; left: 0;">
    <!--
    <text fill="red" :x="x+3" :y="y-15-7" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif">{{ this.$store.getters.getShowAnswer }}</text>
    -->
    <template v-if="box_info.correct === false && showAnswer === true && showans === true ">
        <rect fill="white" :x="x" :y="y-36" :width="100" height=35 />
        <text fill="red" :x="x+3" :y="y-15-7" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif">{{ this.box_info.label }} (x)</text>
        <text fill="green" :x="x+3" :y="y-7" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif">{{this.box_info.gtlabel.cat}}-{{this.box_info.gtlabel.subcat}} (o)</text>
    </template>
    
    <rect id="box" class="bnd" :style="color" style="fill:transparent; stroke-width:1;" :x="x" :y="y" :width="w" :height="h"/>
  </svg>
  
</template>

    <!--<template v-if="showAnswer === true">
      <template v-if="box_info.correct">
        <rect fill="white" :x="x" :y="y-18" :width="w" height=17 />
        <text fill="green" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif" :x="x+3" :y="y-7">{{ this.box_info.label }}</text>
      </template>
      <template v-else>
        <rect fill="white" :x="x" :y="y-36" :width="w" height=35 />
        <text fill="red" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif" :x="x+3" :y="y-22">{{ this.box_info.label }}</text>
        <text fill="black" font-size="11" font-weight="bold" font-family="Avenir, Helvetica, Arial, sans-serif" :x="x+3" :y="y-7">{{this.box_info.gtlabel.cat}}-{{this.box_info.gtlabel.subcat}}</text>
      </template>
      
    </template>-->
<script>
//import { mapGetters } from 'vuex'
export default {
  name: 'BoundingBox',
  props: ['color', 'box_info', 'border', 'circle', 'hover', 'showans'],
  data() {
    return {
      clicked: true,
      selected: false,
      annotated: false,
      showAnswer: this.$store.getters.getShowAnswer,
    }
  },
  mounted() {
    const self = this;
    self.$store.subscribeAction({after: (action) => {
      if (action.type === 'setShowAnswer') {
        self.showAnswer = self.$store.getters.getShowAnswer;
      }
    }})
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
  },

  watch: {
    box_info: {
      deep: true,
      handler() {
        console.log('new box')
      }
    }
  }
}
</script>
