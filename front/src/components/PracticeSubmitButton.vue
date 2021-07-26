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
    Annotate all the images to submit!
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
        if (tempbox.label !== gt) {
          
          tempbox.correct = false
        } else {
          tempbox.correct = true
        }
        //tempbox.showdata = true
      }
      self.updateImageBoxes(boxes)
      self.setShowAnswer(!self.$store.getters.getShowAnswer)
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
      return false;//!this.$store.getters.getIfAllImagesAnnotated
    }
    
  }
}
</script>
