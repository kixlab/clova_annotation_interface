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
      }
      self.updateImageBoxes(boxes)
      //console.log(boxes.map(v => v.label))
      self.setShowAnswer(true/*!this.$store.getters.getShowAnswer*/)
      /*
      axios.post(self.$store.state.server_url + '/api/submit/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( function(){
        var doctype=self.$router.currentRoute.fullPath.split('/')[2];
        self.$router.push('../../annot-done/'+doctype);
      });
      */

      
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
