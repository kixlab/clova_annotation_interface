<template>
 <v-col cols="12">
  <v-card
    tile
    @mousedown="clickDown" @mouseup="clickUp"
    
    >
      <v-row>
        <v-col>
          <div ref="img_container">
          <v-img :src="prac_img" contain style="width: 100%; marginTop: 0; paddingTop: 0;;">
            <drag-select-container selectorClass="bnd" style="height: 100%; width: 100%">
              <template slot-scope="{ startPoint }">
                {{startPoint}}
              <div v-if="image_box" ref="img_box">
                <div v-for="box in image_box" :key="box.id">
                  <div v-if="box.selected === true">
                    <bounding-box circle="no" color="stroke:red; stroke-width:2px; fill:red; fill-opacity:0.1;" :box_info="box"/>
                  </div>
                  <div v-else-if="box.annotated === true && box.hover === false">
                    <bounding-box circle="no" color="stroke:grey; fill:grey; fill-opacity:0.4;" :box_info="box"/>
                  </div>
                  <div v-else-if="box.annotated === true && box.hover === true">
                    <bounding-box circle="no" color="stroke:yellow; fill: rgb(220, 223, 131); fill-opacity: 0.4;" :box_info="box"/>
                  </div>
                  <div v-else>
                    <bounding-box circle="yes" color="stroke:rgb(255, 105, 105); stroke-dasharray:0;" :box_info="box"/>
                  </div>
                </div>
              </div>

              </template>
            </drag-select-container>
          </v-img>
          </div>
        </v-col>

      </v-row>
  </v-card>
  <v-card >
    <br>
    As the receipts are from Indonesia, here are some translations for commonly occuring words: <br>
    <span style="textAlign: left;">
    <b >
    Bayar - Pay <br>
    Tunai - Cash <br>
    Kembalian - Change <br>
    ddd
    </b>
    </span>
  </v-card>
 </v-col>
</template>


<script>
import axios from "axios";
import {mapActions, mapGetters} from 'vuex';
import DragSelect from 'vue-drag-select/src/DragSelect.vue'
import BoundingBox from '@/components/BoundingBox.vue'

export default {
  name: "PracticeImagePanel",
  components: {
    BoundingBox,
    'drag-select-container': DragSelect
  },
  data() {
    return {
      image: this.$store.getters.getImage,
      image_box: this.$store.getters.getImageBoxes,
      initialPosition: [],
      startPoint: [],
      endPoint: [],
      original_box: [],
      width: 0,
      height: 0,

      prac_img: 'http://13.125.191.49:8000/media/receipt/receipt_00300.png',
    };
  },

  mounted() {
    const self = this;
    self.loadNewImage()
    self.image_box = self.$store.getters.getImageBoxes;
    this.loadNewImage(function(self) {
      //self.image = self.$store.getters.getImage;
      self.image_box = self.$store.getters.getImageBoxes;
      self.getInitialPosition();
      

      self.$store.subscribeAction({after: (action) => {
        if (action.type === 'setImageBoxes' || action.type === 'updateAnnotatedBoxes' || action.type === 'updateImageBoxes') {
          self.image_box = self.$store.getters.getImageBoxes;
        }
        //if (action.type)
      }})
    })
    


  },

  watch:{
    curr_image_no: {
      deep: true,
      handler(){
        this.loadNewImage();
        console.log('********** watching!!!')
      }
    }
    
  },
  methods: {
    ...mapActions(['setImage', 'initializeImages', 'setImageBoxes', 'updateImageBoxes',]),
    loadNewImage: function() {
      console.log('load new image')
      const self = this;
      axios.get(self.$store.getters.prac_json_url).then(function(res) {
          var json = res.data;
          var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
          var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height);
          //console.log(img_width, img_height)
          //console.log(self.width, self.height, self.width*img_height/img_width)
          self.setImageBoxes([json, self.width, self.width*img_height/img_width, true]);
          self.original_box = json;
      })
      .catch(function(err) {
        console.log(err);
      });
    },
    loadNewJson: function() {
        console.log('load new json')
      const self = this;
      axios.get(self.$store.getters.prac_json_url).then(function(res) {
          var json = res.data;
          var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
          var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height);
          //console.log(img_width, img_height)
          //console.log(self.width, self.height, self.width*img_height/img_width)
          self.setImageBoxes([json, self.width, self.width*img_height/img_width, true]);
          self.original_box = json;
      })
      .catch(function(err) {
        console.log(err);
      });
    },
    newSize: function() {
      const cont_pos = this.$refs.img_container.getBoundingClientRect()
      const width = cont_pos.right-cont_pos.left
      const height = cont_pos.bottom-cont_pos.top
      this.width = width
      this.height = height

      const img_w = this.original_box.meta === undefined ? this.original_box.image_size.width : (this.original_box.meta.image_size === undefined? this.original_box.meta.imageSize.width:this.original_box.meta.image_size.width);
      const img_h = this.original_box.meta === undefined ? this.original_box.image_size.height :(this.original_box.meta.image_size === undefined? this.original_box.meta.imageSize.height:this.original_box.meta.image_size.height)
      var ratio = 1
      var padding_x = 0
      var padding_y = 0
      if (img_w/width >= img_h/height) {
          ratio = img_w/width
          padding_y = (height-(img_h/ratio))/2
      } else {
          ratio = img_h/height
          padding_x = (width-(img_w/ratio))/2
      }

      var temp_image_box = this.image_box
      for (var box in temp_image_box) {
        var temp = temp_image_box[box]
        temp.x_pos = temp.quad.x1/ratio+padding_x
        temp.y_pos = temp.quad.y1/ratio+padding_y
        temp.x_len = (temp.quad.x2-temp.quad.x1)/ratio
        temp.y_len = (temp.quad.y3-temp.quad.y2)/ratio
      }
      this.updateImageBoxes(temp_image_box)
    },

    getInitialPosition: function() {
      const box_pos = this.$refs.img_box.getBoundingClientRect()
      this.initialPosition = [box_pos.x, box_pos.y]

      const cont_pos = this.$refs.img_container.getBoundingClientRect()
      this.width = cont_pos.right-cont_pos.left
      this.height = cont_pos.bottom-cont_pos.top
    },

    clickDown: function(event) {
      this.startPoint = [event.clientX, event.clientY];
    },

    clickUp: function(event) {
      this.endPoint = [event.clientX, event.clientY];
      this.getInitialPosition();
      this.updateSelectedBoxes();
    },

    updateSelectedBoxes: function() {
      var start, end;
      var boxes = this.image_box;
      if (this.startPoint[0] === this.endPoint[0] && this.startPoint[1] === this.endPoint[1]) {
        for (var i in boxes) {
          var x11 = boxes[i].x_pos;
          var x22 = boxes[i].x_pos + boxes[i].x_len;
          var y11 = boxes[i].y_pos;
          var y22 = boxes[i].y_pos + boxes[i].y_len;
          if (x11-1 < this.startPoint[0]-this.initialPosition[0] && x22+1 > this.startPoint[0]-this.initialPosition[0] && y11-1 < this.startPoint[1]-this.initialPosition[1] && y22+1 > this.startPoint[1]-this.initialPosition[1]) {
            if (boxes[i].annotated === false) {
              boxes[i].selected = !boxes[i].selected;
              if (boxes[i].selected === true) {
                this.$helpers.server_log(this, 'SB', boxes[i].box_id);
              } else {
                this.$helpers.server_log(this, 'UB', boxes[i].box_id);
              }
            }
            this.updateImageBoxes(boxes);
          }
        }
      } else {
      if (this.startPoint[0] <= this.endPoint[0]) {
        if (this.startPoint[1] <= this.endPoint[1]) {
          start = [this.startPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]];
          end = [this.endPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]];
        }
        else {
          start = [this.startPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]];
          end = [this.endPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]];
        }
      } 
      else {
        if (this.startPoint[1] <= this.endPoint[1]) {
          start = [this.endPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]];
          end = [this.startPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]];
        }
        else {
          start = [this.endPoint[0]-this.initialPosition[0], this.endPoint[1]-this.initialPosition[1]];
          end = [this.startPoint[0]-this.initialPosition[0], this.startPoint[1]-this.initialPosition[1]];
        }
      }

      var selected_box = [];
      var unselected_box = [];
      for (var box in boxes) {
        var x1 = boxes[box].x_pos;
        var x2 = boxes[box].x_pos + boxes[box].x_len;
        var y1 = boxes[box].y_pos;
        var y2 = boxes[box].y_pos + boxes[box].y_len;

        //if (start[0] <= x1 && start[0] <= x2 && end[0] >= x1 && end[0] >= x2 && start[1] <= y1 && start[1] <= y2 && end[1] >= y1 && end[1] >= y2) {
        //if (start[0] <= x1 && start[0] <= x2 && end[0] >= x1 && end[0] >= x2 && (start[1] <= y1 || start[1] <= y2) && (end[1] >= y1 || end[1] >= y2)) {
        if ((start[0] <= x1 || start[0] <= x2) && (end[0] >= x1 || end[0] >= x2) && (start[1] <= y1 || start[1] <= y2) && (end[1] >= y1 || end[1] >= y2)) {

          if (this.image_box[box].annotated === false) {
            //this.image_box[box].selected = !this.image_box[box].selected;
            this.image_box[box].selected = true;
            if (this.image_box[box].selected === true) {
              selected_box.push(this.image_box[box].box_id)
            } else {
              unselected_box.push(this.image_box[box].box_id)
            }
          }
        } 
      }
      if (selected_box.length > 0){
        this.$helpers.server_log(this, 'SB', selected_box);
      }
      if (unselected_box.length > 0){
        this.$helpers.server_log(this, 'UB', unselected_box);
      }

      this.updateImageBoxes(this.image_box);
      }
    },
  },
  created() {
    window.addEventListener("resize", this.newSize);
  },
  destroyed() {
    window.removeEventListener("resize", this.newSize);
  },
  

  computed: {
    ...mapGetters(['getImage', 'getImageBoxes', 'getImageRatio', 'curr_image_no']),
    
    /*image_url() {
      return require('http://13.125.191.49:8000/media/receipt/receipt_00300.png')//this.$store.getters.prac_image_url;
    }*/
    
  }
};
</script>

<style scoped>
.instruction {
  text-align: left;
  padding-left: 20px;
  color: black;
}

.red-text {
  color: red;
  font-weight: bold;
}
</style>