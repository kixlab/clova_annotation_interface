<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%">
        <b> 2. Choose a label that best describes the <span >selected box(es)</span>.</b> 
      </v-card-title>
      
      <v-card-subtitle class='text-left'>
        There are <b style="color:blue;">Sub-categories</b> to <b style="color:blue;"> each category</b>. We recommend you take a look at all of them before starting to annotate.
      </v-card-subtitle>
      
      <v-card-text> 
        <v-row>
          <v-col :cols="2" style="text-align:left;">
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

          <v-col :cols="7" style="text-align:left;">
            Sub-category
             <v-list>
              <v-list-item-group
              >
                <v-list-item v-for="subcat in subcats.filter(e=>e.cat == category.cat)" :key="subcat.pk">
                  <span class='subcat-div'>
                    <b>{{subcat.subcat}}</b>: {{subcat.description}}
                    <span v-if="subcat.subcat!='n/a'" class='conf-btn'>
                      <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="annotate(subcat, 1, '')">Exactly</v-btn>
                      <v-btn x-small outlined color="warning" style='margin-right:1px;' v-on:click.stop="openSuggestion(subcat.pk)">Close to</v-btn>
                      <div v-if="subcat.suggestion" :id="'suggestion-'+subcat.pk" class='suggestion-holder'>
                        <suggestion  v-bind:subcat="subcat"  v-bind:confidence=0 @annotate="annotate" @done="closeSuggestion(subcat.pk)"/>
                      </div>
                    </span>
                    <span v-if="subcat.subcat=='n/a'" class='conf-btn'>
                        <v-btn x-small outlined color="error" style='margin-right:1px;' v-on:click.stop="openSuggestion(subcat.pk)">N/A</v-btn>
                        <div v-if="subcat.suggestion" :id="'suggestion-'+subcat.pk" class='suggestion-holder'>
                        <suggestion  v-bind:subcat="subcat" v-bind:confidence='null' @annotate="annotate" @done="closeSuggestion(subcat.pk)"/>
                      </div>
                    </span>
                  </span>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
          <v-col :cols="3" style="text-align:left;">
            </v-col>
        </v-row>
      </v-card-text>

    </v-card>
  </v-col>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import axios from "axios";
import Suggestion from '@/components/Suggestion.vue'

export default {
  name: 'DeferredAnnotation',
  components: {
    Suggestion
  },
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
      axios.get(self.$store.state.server_url+'/api/get-annotations/',{
        params:{
          mturk_id: self.$store.state.mturk_id,
          doctype: self.$route.params.docType,
          image_id: self.$store.state.curr_image_no
        }
      }).then(function(res){
        var annotations=res.data.annotations;
        self.loadAnnotatedBoxes(annotations);})}
    ,1000);
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

      openSuggestion(subcatpk){
        //find idx 
        var idx = 0;
        for(let i =0;i<this.subcats.length;i++){
          if(this.subcats[i].pk===subcatpk){
            idx=i;
          }
        }
        this.subcats[idx]["suggestion"]=true
      },
      closeSuggestion(subcatpk){
        var idx = 0;
          for(let i =0;i<this.subcats.length;i++){
            if(this.subcats[i].pk===subcatpk){
              idx=i;
            }
          }
          this.subcats[idx]["suggestion"]=false
      },

      annotate(item, confidence, suggestion) {

        const imageBox = this.getImageBoxes()//this.image_box
        var group = []
        var label = item.cat + "-" + item.subcat
        if(confidence!=1){
          label=label+' (suggested: '+ suggestion+')'
        }
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

        //this.$helpers.server_log(this, 'CL', group.map((i) => {return i.box_id}), label)
        this.updateImageBoxes(this.image_box)

        if(group.length>0){
          axios.post(self.$store.state.server_url + "/api/save-annotation/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.curr_image_no,
            boxes_id: group.map((i) => {return i.box_id}),
            subcatpk:subcatpk,
            catpk: catpk,
            confidence: confidence,
            suggestion: suggestion
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
        axios.get(self.$store.state.server_url+'/api/get-annotations/',{
          params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.curr_image_no
          }
        }).then(function(res){
          var annotations=res.data.annotations;

          setTimeout(self.loadAnnotatedBoxes(annotations),1000);

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

.suggestion-holder{
  padding: 5px;
  position: absolute;
  display: inline;
  width: 175px;
}
</style>