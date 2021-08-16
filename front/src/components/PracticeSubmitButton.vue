<template>
  <v-tooltip bottom :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :disabled="disabled"
        color="green"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Check answer
      </v-btn>
      </div>
    </template>
    Annotate all boxes to check answer!
  </v-tooltip>
</template>

<script>
//import axios from "axios";
import {mapGetters, mapActions} from 'vuex';

export default {
  name: "SubmitButton",
  methods: {
    ...mapGetters(['getIfAllImagesAnnotated']),
    ...mapActions(['updateImageBoxes', 'setShowAnswer']),

    onSubmit: function() {
      const self=this;
      //console.log(self.$store.getters.getImageBoxes)
      var boxes = self.$store.getters.getImageBoxes
      for (var box in boxes) {
        var tempbox = boxes[box]
        var gt = tempbox.gtlabel.cat + '-' + tempbox.gtlabel.subcat
        //console.log(tempbox.label, "vs.", gt)
        if (tempbox.label !== gt) {
          tempbox.correct = false
        } else {
          tempbox.correct = true
        }
        tempbox.anschecked = true
      }
      var accuracy = (boxes.filter(v => v.correct).length / 22.0 * 100).toFixed(2)
      var wrong = 22 - boxes.filter(v => v.correct).length
      if (wrong > 0) {
        alert("You are " + accuracy + "% correct. Please check the answers to the " + wrong + " boxes that you incorrectly labeled on the image.")
      }
      else {
        alert("You got everything correct! Please move on to the actual task. Good job!! 😊")
      }
      
      self.updateImageBoxes(boxes)
      //console.log(boxes.map(v => v.label))
      self.setShowAnswer(true/*!this.$store.getters.getShowAnswer*/)
      
    }
  },

  computed: {
    
    disabled() {
      //console.log(this.$store.getters.getAnnotatedBoxes.map(v => v.boxes).flat(1).map(v => v.box_id).length >= 22)
      return this.$store.getters.getAnnotatedBoxes.map(v => v.boxes).flat(1).length < 22
    }
    
  }
}
</script>
