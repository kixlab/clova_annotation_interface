<template>
  <v-col cols="12">
    <v-card tile>
      <v-card-title style="font-size: 110%">
        <b> 2. Choose a label that best describes the <span class="red-text">selected box(es)</span>.</b> 
      </v-card-title>
      
      <v-card-subtitle class='text-left'>
        There are <b style="color:blue;">10 categories</b> and <b style="color:red;">N/A</b>. Please scroll down to take a look at all of them.
      </v-card-subtitle>
      
      <v-card-text> 
        <v-row>
          <v-col :cols="4" style="text-align:left;">
            Category
            <v-list >
              <v-list-item-group
                v-model='sel_category'
                active-class="border"
                color="indigo"
              >
                <v-list-item v-for="category in cats" :key='category.pk' @click="selectCategory(category)">
                  <span v-if="!category.rev">
                    <b>{{category.cat}}</b> 
                    <v-btn v-if="category.usermade" x-small class='rev-btn' v-on:click.stop="initCatRev(category.pk)">
                      <v-icon
                        x-small
                        color='indigo'
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                  </span>
                  <span v-if="category.rev" class='rev-div'>
                    <v-text-field :value="category.cat" :id="'revcat_'+category.pk"></v-text-field>
                    <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="revCat(category.pk)">V</v-btn>
                    <v-btn x-small outlined color="red" v-on:click.stop="cancelCatRev(category.pk)">X</v-btn>
                  </span>
                </v-list-item>
                <v-list-item v-if="isAdding">
                  <v-text-field label="new category" id='newCat'></v-text-field>
                  <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="addCategory()">+ add</v-btn>
                  <v-btn x-small outlined color="red" v-on:click.stop="cancelAdd()">X</v-btn>
                </v-list-item>
                <v-list-item v-if="!isAdding" v-on:click.stop="getCategory()"><b>+</b> add</v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>

          <v-col :cols="8" style="text-align:left;">
            Sub-category
             <v-list>
              <v-list-item-group
                active-class="border"
                color="indigo"
              >
                <v-list-item v-for="subcat in subcats.filter(e=>e.cat == category.cat)" :key="subcat.pk" @click="annotate(subcat, subcat.rev)">
                  <span v-if="!subcat.rev">
                    <b>{{subcat.subcat}}</b>: {{subcat.description}} 
                    <v-btn v-if="subcat.usermade" x-small class='rev-btn' v-on:click.stop="initSubRev(subcat.pk)">
                      <v-icon
                        x-small
                        color='indigo'
                      >
                        mdi-pencil
                      </v-icon>
                    </v-btn>
                  </span>
                  <span v-if="subcat.rev" class='rev-div'>
                    <v-text-field :value="subcat.subcat" :id='"revsubcat_"+subcat.pk'></v-text-field>
                    :
                    <v-text-field :value="subcat.description" :id='"revdesc_"+subcat.pk'></v-text-field>
                    <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="revSubcat(subcat.pk)">V</v-btn>
                    <v-btn x-small outlined color="red" v-on:click.stop="cancelSubRev(subcat.pk)">X</v-btn>
                  </span>
                </v-list-item>
                <v-list-item v-if="isAddingSub">
                  <v-text-field label="new subcategory" id='newSubCat'></v-text-field>
                  :
                  <v-text-field label="description" id='newDesc'></v-text-field>
                  <v-btn x-small outlined color="success" style='margin-right:1px;' v-on:click.stop="addSubCategory()">+ add</v-btn>
                  <v-btn x-small outlined color="red" v-on:click.stop="cancelAddSub()">X</v-btn>
                </v-list-item>
                <v-list-item v-if="isCategorySelected&&(!isAddingSub)" v-on:click.stop="getSubCategory()"><b>+</b> add</v-list-item>
              </v-list-item-group>
            </v-list>
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
  name: 'Labeling',
  data() {
    return{
      selection: [],
      subcats: [
          { id: 1, label: 'menu', sublabel: 'id', description: 'ID of the menu'},
          { id: 2, label: 'menu', sublabel: 'name', description: 'Name of the menu'},
          { id: 3, label: 'menu', sublabel: 'unit price', description: 'Unit price of the menu'},
          { id: 4, label: 'menu', sublabel: 'count', description: 'Number of the menu consumed'},
          { id: 5, label: 'menu', sublabel: 'price', description: 'Total price of the menu'},
          { id: 6, label: 'subtotal', sublabel: 'menu count', description: 'Number of unique menus'},
          { id: 7, label: 'subtotal', sublabel: 'item count', description: 'Number of items'},
          { id: 8, label: 'subtotal', sublabel: 'price', description: 'Subotal price excluding tax'},
          { id: 9, label: 'subtotal', sublabel: 'service charge', description: 'Service charge'},
          { id: 10, label: 'subtotal', sublabel: 'tax price', description: 'Tax price'},
          { id: 11, label: 'total', sublabel: 'total price', description: 'Total price'},
          { id: 12, label: 'payment', sublabel: 'cash payment', description: 'Price paid by cash'},
          { id: 13, label: 'payment', sublabel: 'credit card payment', description: 'Price paid by credit card'},
          { id: 14, label: 'payment', sublabel: 'change', description: 'Amount of change received'},
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
        image_id: self.$store.state.image_order + self.$store.state.start_image_no
      }
    }).then(function(res){
      var annotations=res.data.annotations;
      self.loadAnnotatedBoxes(annotations);})},1000);
  },
  methods: {
      ...mapActions(['updateImageBoxes', 'updateAnnotatedBoxes', 'setAStatus']),
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

      addCategory(){
        this.addcat=false;
        var newcat=document.getElementById('newCat').value;
        const self = this;

        axios.post(self.$store.state.server_url + "/api/add-cat/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no,
            cat: newcat
          }).then(function (res) {
            self.cats.push({cat: newcat, pk:res.data.newcat_pk,usermade:true, rev:false});
          });                
      },
       addSubCategory(){
        this.addsubcat=false;
        var newsubcat=document.getElementById('newSubCat').value;
        var newdesc=document.getElementById('newDesc').value;
        var cat=this.category.cat;
        const self = this;

        axios.post(self.$store.state.server_url + "/api/add-subcat/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no,
            cat: cat,
            subcat: newsubcat,
            description: newdesc
          }).then(function (res) {
            self.subcats.push({cat: cat, subcat: newsubcat, description: newdesc, pk:res.data.newsubcat_pk, usermade:true, rev:false});        
          });
      },
      resetAddState(){
        for (var idx in this.cats){
          var cat=this.cats[idx]
          cat.rev=false;
        }
      },
      cancelCatRev(cat_pk){
        for (var idx in this.cats){
          var cat=this.cats[idx]
          if(cat.pk==cat_pk){
            cat.rev=false;
          }
        }

      },
      initCatRev(cat_pk){
        for (var idx in this.cats){
          var cat=this.cats[idx]
          if(cat.pk==cat_pk){
            cat.rev=true;
          }
        }
      },
      cancelSubRev(subcat_pk){
        for (var idx in this.subcats){
          var subcat=this.subcats[idx]
          if(subcat.pk==subcat_pk){
            subcat.rev=false;
          }
        }
      },
      initSubRev(subcat_pk){
        for (var idx in this.subcats){
          var subcat=this.subcats[idx]
          if(subcat.pk==subcat_pk){
            subcat.rev=true;
            console.log('initsubrev', subcat)
          }
        }
      },
      revCat(cat_pk){
        var revcat=document.getElementById('revcat_'+String(cat_pk)).value;
        const self=this;
        for (var idx in this.cats){
          var cat=this.cats[idx]
          if(cat.pk==cat_pk){
            var oldcat=cat.cat
                cat.cat=revcat;
                cat.rev=false;
                //self.subcats.push({cat: cat, subcat: newsubcat, description: newdesc, pk:res.data.newsubcat_pk, usermade:true, rev:false});
                for (var subidx in this.subcats){
                  var subcat=this.subcats[subidx]
                  if(subcat.cat==oldcat){
                    subcat.cat=revcat;
                  }
            }        
          }
        }
        axios.post(self.$store.state.server_url + "/api/revise-cat/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            cat_pk: cat_pk,
            revcat: revcat
          });
      },
      revSubcat(subcat_pk){
        var revsubcat=document.getElementById('revsubcat_'+String(subcat_pk)).value;
        var revdesc=document.getElementById('revdesc_'+String(subcat_pk)).value;
        const self=this;
        for (var idx in this.subcats){
          var subcat=this.subcats[idx]
          if(subcat.pk==subcat_pk){
                subcat.subcat=revsubcat;
                subcat.description=revdesc;
                subcat.rev=false;
          }
        }
        axios.post(self.$store.state.server_url + "/api/revise-subcat/", {
          mturk_id: self.$store.state.mturk_id,
          doctype: self.$route.params.docType,
          subcat_pk: subcat_pk,
          revsubcat: revsubcat,
          revdesc: revdesc
        });
      },
      cancelAdd(){
        this.addcat=false;
      },
      add() {
        this.$refs.form.validate()
        
        var id = this.subcats.length
        this.subcats.push({checked: false, id: id, label: this.label, description: this.description})
        
        this.label = '';
        this.description = '';
      },

      annotate(item, revstat) {
        if(!revstat){
        const imageBox = this.getImageBoxes()//this.image_box
        var group = []
        var label = item.cat + "." + item.subcat
        var labelpk=item.pk
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

        this.updateImageBoxes(this.image_box)

        if(group.length>0){
          axios.post(self.$store.state.server_url + "/api/save-annotation/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no,
            boxes_id: group.map((i) => {return i.box_id}),
            labelpk:labelpk
          }).then(function (res) {
            self.updateAnnotatedBoxes([{cat: item.cat, subcat: item.subcat, labelpk: item.pk, catpk:catpk, boxes: group, annotpk: res.data.annot_pk}, "add"])            
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
            image_id: self.$store.state.image_order + self.$store.state.start_image_no,
            status: true
          }).then(function () {
            self.setAStatus({
              'idx':self.$store.state.image_order,
              'val':true
            });
            //console.log('### setAStatus called - annotate')
          });
        }
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
            //console.log(currImageBox)
            self.updateImageBoxes(currImageBox)
            self.updateAnnotatedBoxes([{cat: agroup.cat, subcat: agroup.subcat, labelpk: agroup.subcatpk, catpk: agroup.catpk, boxes: group, annotpk: agroup.group_id}, "add"])
          }          
        },
      clicked(label) {
        console.log("Clicked", label)
      }
  },
  computed: {
    ...mapGetters(['image_no']),

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
    }
  },
  watch:{
    curr_image_no:{
      deep: true,
      handler(){
        const self=this;
        axios.get(self.$store.state.server_url+'/api/get-annotations/',{
          params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
            image_id: self.$store.state.image_order + self.$store.state.start_image_no
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

.rev-btn{
  margin: 0 !important;
  padding: 0 !important;
  outline: 0 !important;
  box-shadow: none !important;
  background-color: transparent !important;
  right: 0 !important;
  position: absolute;
}

.rev-div{
  display:contents !important;
}

th {
  text-align: center; 
  background-color: lightGrey;
}
</style>