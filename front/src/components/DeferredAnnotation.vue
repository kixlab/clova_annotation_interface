<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%">
        <b> 2. Choose a label that best describes the <span class="red-text">selected box(es)</span>.</b> 
      </v-card-title>
      
      <v-card-subtitle class='text-left'>
        There are <b style="color:blue;">Sub-categories</b> to <b style="color:blue;"> each category</b>. We recommend you take a look at all of them before starting to annotate.
      </v-card-subtitle>
      
      <v-card-text> 
        <v-row>
          <v-col :cols="3" style="text-align:left;">
            Category
            <v-list >
              <v-list-item-group
                v-model='sel_category'
                active-class="border"
                color="indigo"
              >
                <v-list-item v-for="category in cats" :key='category.pk' @click="selectCategory(category)">
                    <b>{{category.cat}}</b> 
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>

          <v-col :cols="8" style="text-align:left;">
            Sub-category
             <v-list>
              <v-list-item-group
              >
                <v-list-item v-for="subcat in subcats.filter(e=>e.cat == category.cat)" :key="subcat.pk">
                  <span class='subcat-div'>
                    <b>{{subcat.subcat}}</b>: {{subcat.description}}
                    <span v-if="subcat.subcat!='n/a'" class='conf-btn'>
                    <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="annotate(subcat, 1)">Exactly</v-btn>
                    <v-menu> 
                      <template v-slot:activator="{ on: menu, attrs }">
                        <v-tooltip bottom> 
                        <template v-slot:activator="{ on:tooltip }">
                          <v-btn x-small outlined color="warning" v-on="{ ...tooltip, ...menu }" v-bind="attrs">
                            Can be
                          </v-btn>
                        </template>
                        <span>tooltip</span>
                      </v-tooltip>
                      </template>
                      <v-list>
                        suggestions
                        <v-list-item> hi </v-list-item>
                      </v-list>
                      </v-menu>
                    </span>
                    <span v-if="subcat.subcat=='n/a'" class='conf-btn'>
                        <v-btn x-small outlined color="error" style='margin-right:1px;' v-on:click.stop="annotate(subcat, null)">N/A</v-btn>
                    </span>
                  </span>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
          <v-col :cols="1" style="text-align:left;">
            </v-col>
        </v-row>
         <!-- <v-row>
          <v-col class="text-left">
            <div v-for="category in table" :key="category" style="padding: 4px;">
              <v-menu open-on-hover right offset-x>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    class="text-none"
                    color="normal"
                    small
                    v-bind="attrs"
                    v-on="on"
                  >
                    {{ category }}
                  </v-btn>
                </template>
                <v-list dense>
                  <v-list-item
                    v-for="(item, index) in labelTable.filter(e => e.label == category)"
                    :key="index"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-btn class="text-none" color="normal" small text @click="clicked(item.sublabel); annotate(item)" :disabled=isDisabled>
                        {{ item.sublabel }}
                        </v-btn>
                      </v-list-item-title>
                      <v-list-item-subtitle>{{ item.description }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
              <br/>
            </div>
          </v-col>
        </v-row>

        <v-row>
          <v-col class="text-left">
            <v-autocomplete
              clearable
              dense
              filled
              :items="labelTable"
              label="Search for the label.."
            >
              <template v-slot:selection="data">
                {{ data.item.label.concat(' - ', data.item.sublabel) }}
              </template>
              <template v-slot:item="data">
                
              </template>
            </v-autocomplete>
          </v-col>
        </v-row> -->

        <!-- <v-row>
          <v-col>
            <v-simple-table fixed-header height="250px">
                <template v-slot:default>
                <thead>
                    <tr>
                      <th style="textAlign: center; background-color: lightGrey;"></th>
                      <th style="textAlign: center; background-color: lightGrey;">#</th>
                      <th style="textAlign: center; background-color: lightGrey;">Category</th>
                      <th style="textAlign: center; background-color: lightGrey;">Label</th>
                      <th style="textAlign: center; background-color: lightGrey;">Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in labelTable" :key="item.id">
                      <td style="padding:0; width: 35px;">
                        <v-tooltip top>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn small icon color="darkgrey" @click="annotate(item)" :disabled=isDisabled v-bind="attrs" v-on="on">
                              <v-icon>check_circle</v-icon>
                            </v-btn>
                          </template>
                          <span>annotate</span>
                        </v-tooltip>
                      </td>
                      <td style="background-color: #eee">{{ item.id }}</td>
                      <td>{{ item.label }}</td>
                      <td style="background-color: #eee">{{ item.sublabel }}</td>
                      <td>{{ item.description }}</td>
                        
                    </tr>
                </tbody>
                </template>
            </v-simple-table>
          </v-col>
        </v-row> -->
      </v-card-text>

    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from "axios";

export default {
  name: 'DeferredAnnotation',
  data() {
    return{
      selection: [],
      subcats: [
      ]   ,
      selected_boxes: this.$store.getters.getSelectedBoxes,
      image_box: this.$store.getters.getImageBoxes,
      cats: ['menu', 'subtotal', 'total', 'payment'],
      category:'',
      subcategory:'',
      addcat: false,
      addsubcat: false,
      sel_category: null,    
  }},
  mounted: function () {
    const self = this;
    this.$store.subscribeAction((action) => {
      if (action.type === 'updateImageBoxes') {
          this.image_box = this.$store.getters.getImageBoxes
      }
    })

    axios.get(self.$store.state.server_url + "/api/get-cats",{
      params:{
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType
      }
    }).then(function(res){
      self.cats=res.data.cats;
      self.subcats=res.data.subcats;
      self.category=self.cats[0];
      })
    
    setTimeout( function(){
    axios.get(self.$store.state.server_url+'/api/get-def-annotations/',{
      params:{
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType,
        image_id: self.$store.state.curr_image_no
      }
    }).then(function(res){
      var annotations=res.data.annotations;
      self.loadAnnotatedBoxes(annotations);})},1000);
  },
  methods: {
      ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes', 'setAStatus', 'setStatus']),
      ...mapGetters(['getImageBoxes']),

      selectCategory(selectedCategory){
        this.category=selectedCategory;
        this.addsubcat=false;
      },

      getCategory(){
        this.category='';
        this.addcat=true;
      },
      getSubCategory(){
        this.subcategory='';
        this.addsubcat=true;
      },

      
      annotate(item, confidence) {

        const imageBox = this.getImageBoxes()//this.image_box
        var group = []
        var label = item.cat + "." + item.subcat
        var subcatpk=item.pk
        var catpk=item.catpk
        const self = this;

        for (var box in imageBox) {
            if (imageBox[box].selected === true) {
                var currBox = this.image_box[box]
                currBox.label = label
                currBox.selected = false
                currBox.annotated = true
                group.push(currBox)
            }
        }

        this.$helpers.server_log(this, 'CL', group.map((i) => {return i.box_id}), label)
        this.updateImageBoxes(this.image_box)

        if(group.length>0){
          axios.post(self.$store.state.server_url + "/api/save-def-annotation/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.curr_image_no,
            boxes_id: group.map((i) => {return i.box_id}),
            subcatpk:subcatpk,
            catpk: catpk,
            confidence: confidence
          }).then(function (res) {
            self.updateAnnotatedBoxes([{cat: item.cat, subcat: item.subcat, subcatpk: item.pk, catpk:catpk, boxes: group, confidence: confidence, annotpk: res.data.annot_pk}, "add"])            
          });
        }else{
          window.alert("Please select boxes to annotate.")
        }
        //self.category='';
        //self.sel_category=null;
        self.subcategory='';

        if(this.$store.getters.getIfAllBoxesAnnotated){
          axios.post(self.$store.state.server_url + "/api/update-status/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.curr_image_no,
            status: true
          }).then(function () {
            self.setAStatus({
              'idx':self.$store.state.image_order,
              'val':true
            });
          });
        }
      },

      loadAnnotatedBoxes(annotations){
        const self = this;
          self.updateAnnotatedBoxes([[], "reset"])
          var currImageBox = self.$store.getters.getImageBoxes
          for (var gno in annotations){
            var agroup=annotations[gno]
            var group=[]
            var ids=agroup.boxes_id.replace("[","").replace("]","").replace(" ","").replace(', ',',').split(',')
            for(var id in ids){
              var box_id=parseInt(ids[id])
              var currBox=currImageBox[box_id]
              if((currBox==undefined)||(currBox.box_id!=box_id)){
                currBox=currImageBox[box_id-1];
              }
              currBox.annotated=true
              group.push(currBox)
            }
            self.updateImageBoxes(currImageBox)
            self.updateAnnotatedBoxes([{cat: agroup.cat, subcat: agroup.subcat, subcatpk: agroup.subcatpk, catpk: agroup.catpk, boxes: group, confidence: agroup.confidence, annotpk: agroup.group_id}, "add"])
          }          
        },
  },
  computed: {
    ...mapGetters(['getImage','getImageRatio', 'get_image_order', 'get_curr_image']),
    isDisabled() {
        return this.$store.getters.getSelectedBoxes.length === 0
    },
    isCategorySelected(){
      return (this.category!='')
    },
    isSubSelected(){
      return (this.subcategory!='')
    },
    isAdding(){
      return (this.addcat)
    },
    isAddingSub(){
      return (this.addsubcat)
    },
  },
  watch:{
    get_curr_image:{
      deep: true,
      handler(){
        const self=this;
        axios.get(self.$store.state.server_url+'/api/get-def-annotations/',{
          params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.curr_image_no
          }
        }).then(function(res){
          var annotations=res.data.annotations;
          
          setTimeout(
          self.loadAnnotatedBoxes(annotations),1000);

    })
  }}},
}
</script>
<style scoped>

.instruction {
  text-align: left;
  padding-left: 20px;
}
.red-text {
  color:red;
  font-weight: bold;
}
.btn {
  margin-left: 1rem;
}

.conf-btn{
  margin: 0 !important;
  padding: 0 !important;
  outline: 0 !important;
  box-shadow: none !important;
  background-color: transparent !important;
  right: 0 !important;
  position: absolute;
}

.subcat-div{
  display:contents !important;
}

th {
  text-align: center; 
  background-color: lightGrey;
}
</style>