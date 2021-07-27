<template>
<v-card class='suggestion-holder'>
  <v-container fluid style='padding:0'>
      <v-row
      >
      <v-col cols='12' style='padding:0'>
          <v-btn
            x-small outlined
            color="error" 
            class="close-btn">
            X
          </v-btn>
      </v-col>
      </v-row>
  </v-container>
  <v-container>
      <v-row>
        <v-col cols="12">
          
          <v-combobox
            v-model="value"
            :items="suggestions"
            :item-text="item => `${item.suggested_subcat} `"
            dense
          >
            <template v-slot>
            {{ suggestion }}
          </template>
          </v-combobox>
        </v-col>
      </v-row>
  </v-container>
  <v-container style='padding:0'>
      <v-row
      >
      <v-col cols='12' style='padding:0'>
          <v-btn
            x-small outlined
            color="primary" 
            class="close-btn" v-on:click.stop="markSuggestion">
            Suggest
          </v-btn>
      </v-col>
      </v-row>
  </v-container>
  
    </v-card>
</template>

<script>
//import { mapActions, mapGetters} from 'vuex'
import axios from "axios";


export default {
  name: "Suggestion",
  props: ['subcat', 'confidence'],
  data: () => ({
      mysuggestions: [],
      othersuggestions: [],
      suggestions:[],
      value: {'suggested_subcat': ''},
    }),
  mounted: function(){
    const self=this;
    axios.get(self.$store.state.server_url + '/api/get-suggestions/',{
      params:{
        mturk_id: self.$store.state.mturk_id, 
        doctype: self.$route.params.docType, 
        subcatpk: self.subcat.pk
      }
    }).then(function(res){
      self.mysuggestions=res.data.mysuggestions;
      self.othersuggestions=res.data.othersuggestions;
      var suggestions = res.data.mysuggestions.concat(res.data.othersuggestions)
      self.suggestions=suggestions;
      console.log(suggestions)
    })

  },
  methods:{
    markSuggestion: function(){
      this.$emit('annotate', this.subcat, this.confidence, this.value);}
  }
};
</script>

<style scoped>
.close-btn{
  padding:5 !important;
  min-width: 0px !important;
  position: absolute;
  right: 0;
}
</style>
