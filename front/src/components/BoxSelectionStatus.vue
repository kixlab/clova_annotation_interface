<template>
    <v-col cols="12">
      <v-progress-linear
        color="lime"
        style="margin-bottom: 10px"
        :value="annot_progress"
        :height="25"
      >
        <b>
        {{ annot_progress }}% 
          (
            <span style="color: red">{{image_box_num - image_box_todo_num}}</span>
          / {{image_box_num}} boxes
          )
        </b>
      </v-progress-linear>

      <v-card tile>
      <v-card-title style="font-size: 110%" class="text-left"><b>
        1. Drag or click to select <span class="red-text">red box(es)</span> on the image.</b> 
      </v-card-title>
      <v-card-subtitle class='text-left'>
        You should <b style="color:blue;">select one group of box(es) at a time</b> that indicates a single entity.<br>
      </v-card-subtitle>
      <v-card-text style="min-height:130px; max-height: 200px; text-align:left; overflow-y: scroll;" scrollable>
        <div class="text-left" style="font-size: 100%; padding: 5px;"> 
          <b style="color:gray">Selected boxes: </b>
          <div style="display:flex;" class="flex-wrap"> 
          <div v-for="box in selected_box" :key="box.id" >
              <span style="border: 2px solid red; margin: 0 2px; font-size: 95%; padding: 0 3px;"> <b>{{ box.text }}</b> </span>
          </div>
          </div>
          <br/>
          <v-btn 
            :disabled="selected_box.length === 0"
            @click="unselect"
            small 
            color="secondary" 
            depressed>
            Undo all selections
            </v-btn> 
        </div>
      </v-card-text>
  </v-card>
    </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
    name: "BoxSelectionStatus",
    data() {
        return {
          image_box : this.$store.getters.getImageBoxes,
        };
    },

    mounted() {
      this.$store.subscribeAction({after: (action) => {
        if (action.type === 'setImageBoxes' || action.type === 'updateAnnotatedBoxes' || action.type === 'updateImageBoxes') {
          this.image_box = this.$store.getters.getImageBoxes;
        }
      }})

    },

    methods: {
        ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes']),
        ...mapGetters(['getImageBoxes']),

        highlight(item) { item.hover = true },
        undoHighlight(item) { item.hover = false },

        highlightGroup(group) {
            for (var box in group) {
                group[box].hover = true
            }
        },

        unselect: function() {
          var boxes = this.image_box;
          var selected_boxes = [];
          for (var i in boxes) {
            if (boxes[i].selected === true) {
              boxes[i].selected = false
              selected_boxes.push(parseInt(i));
            }
          }
          this.$helpers.server_log(this, 'UA', selected_boxes);
          this.updateImageBoxes(boxes);
        },
    },
    computed: {
        selected_box() {
          return this.$store.getters.getImageBoxes.filter(v=>v.selected);
        },
        image_box_num () {
            return this.image_box.length;
        },
        image_box_todo_num () {
            return this.image_box.filter(v=>v.annotated === false).length;
        },
        annot_progress () {
            return 100-Math.ceil((this.image_box_todo_num/this.image_box_num)*100);
        }
    }
    
}
</script>
