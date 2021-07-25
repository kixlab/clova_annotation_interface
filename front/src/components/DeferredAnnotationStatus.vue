<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%" class="text-left"><b>3. Hover to see corresponding boxes on the image.</b> </v-card-title>
      <v-card-text style="min-height:200px; text-align:left;" scrollable>
        <div v-if="isAnnotationExist">
            No annotations yet for this image :-(
        </div>
        <div v-else>
          <v-dialog
            v-model="undo_warning"
            width = "500px"
          >
            <template v-slot:activator="{on, attrs}">
              <v-btn 
                small 
                color="secondary" 
                depressed 
                v-bind = "attrs"
                v-on = "on"
                style="margin-bottom: 10px"> Undo all annotations 
              </v-btn>
            </template>
              <v-card>
              <v-card-title/>
              <v-card-text style="text-align:left; font-size:large; color:red;">
                <b>Are you sure you want to undo all annotations? <br/>You cannot revert this action.</b>
              </v-card-text>
              <v-card-actions>
                <v-btn
                  color="error darken-1"
                  text
                  @click="reset"
                >
                  Yes, I want to
                </v-btn>
                <v-spacer/>
                <v-btn
                  color="green darken-1"
                  text
                  @click="undo_warning = false"
                >
                  No, I don't want to
                </v-btn>
              </v-card-actions>
              </v-card>
            </v-dialog>
              
            
          <div v-for="group in annotated_box" :key="group.id" :id="'annot_'+group.annotpk">
            <v-btn-toggle dense style="padding:5px" class="flex-wrap" >
              <v-btn text small tile depressed @mouseover="highlightGroup(group.boxes)" @mouseout="undoHighlightGroup(group.boxes)" style="border: 0.1px solid #eeeeee !important;" v-bind:class="{success: group.confidence, error: (group.subcat=='N/A'), warning: !group.confidence}"> 
                {{group.cat}}-{{group.subcat}} 
              </v-btn>
              
              <div v-for="box in group.boxes" :key="box.id">
                <v-btn small tile depressed @mouseover="highlight(box)" @mouseout="undoHighlight(box)" style="padding:0 3.5px; min-width:0px; border: 0.1px solid #eaeaea !important; font-size:80%; background-color: #f1f1f1"> 
                  {{box.text}}  
                </v-btn>
              </div>
              <v-tooltip right>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn small depressed icon @click="remove(group)" v-bind="attrs" v-on="on"> <v-icon>delete_outline</v-icon> </v-btn>
                </template>
                <span>remove annotation</span>
              </v-tooltip>
            </v-btn-toggle>
          </div>
        </div>

      </v-card-text>
    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from "axios";


export default {
    name: "LabeledBoxes",
    data() {
      return {
          image_box: this.$store.getters.getImageBoxes,
          annotated_box: this.$store.getters.getAnnotatedBoxes,
          undo_warning: false,
      };
    },

    mounted() {
      this.$store.subscribeAction({after: (action) => {
        if (action.type === 'updateImageBoxes') {
          this.image_box = this.$store.getters.getImageBoxes;
        }
        if (action.type === 'updateAnnotatedBoxes') {
          this.annotated_box = this.$store.getters.getAnnotatedBoxes;
        }
          
      }})

    },


  methods: {
    ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes', 'setAStatus', 'setStatus']),
    ...mapGetters(['getImageBoxes']),

    highlight(item) { item.hover = true },
    undoHighlight(item) { item.hover = false },

    highlightGroup(group) {
      for (var box in group) {
          group[box].hover = true;
      }
    },

    undoHighlightGroup(group) {
      for (var box in group) {
          group[box].hover = false;
      }
    },

    remove(group) {
      const self = this;
      axios.post(self.$store.state.server_url + "/api/delete-def-annotation/", {
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType,
        image_id: self.$store.state.curr_image_no,
        annot_pk: group.annotpk
      }).then(function () {
//        console.log("Annotation deleted", res.data.annot_pk)
        for (var i in self.image_box) {
          var temp = self.image_box[i]
          for (var box in group.boxes) {
            var removedBox = group.boxes[box]
            if (temp.x_pos === removedBox.x_pos && temp.y_pos === removedBox.y_pos) {
              temp.annotated = false;
              temp.label = '';
            }
          }
        }
        self.$helpers.server_log(self, 'RA', group.boxes.map((i) => {return i.box_id}))
        self.updateImageBoxes(self.image_box)
        self.updateAnnotatedBoxes([group, "remove"])
      });

      axios.post(self.$store.state.server_url + "/api/update-status/", {
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType,
        image_id: self.$store.state.curr_image_no,
        status: false
      }).then(function () {
        //console.log('set status false')
        //console.log('idx', self.$store.state.image_order)
        //console.log(self.$store.state.annot_status)
        self.setAStatus({
          'idx':self.$store.state.image_order,
          'val':false
        });
      });
  

    },

    reset() {
      for (var i in this.image_box) {
        var temp = this.image_box[i];
        temp.annotated = false;
        temp.label = '';
      }

      this.$helpers.server_log(this, 'RL', [])
      this.updateImageBoxes(this.image_box)
      this.updateAnnotatedBoxes([[], "reset"])
      this.undo_warning = false;
    }


  },
  computed: {
    isAnnotationExist () {
        return (this.annotated_box.length < 1)
    }
  }

    
}
</script>

<style scoped>

.error.warning{
  background-color: #ff5252 !important;
  color: white !important;

}
</style>

