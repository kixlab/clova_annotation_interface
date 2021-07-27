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
            :item-text="item => `${item.suggestion} `"
            dense
          >
            <template v-slot>
            {{ data.suggestion }}
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
            class="close-btn" v-on:click.stop="submitSuggestion">
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
  props: ['subcatpk'],
  data: () => ({
      mysuggestions: [],
      othersuggestions: [],
      suggestions:[],
      value: null,
    }),
  mounted: function(){
    const self=this;
    axios.get(self.$store.state.server_url + '/api/get-suggestions/',{
      params:{
        mturk_id: self.$store.state.mturk_id, 
        doctype: self.$route.params.docType, 
        subcatpk: self.subcatpk
      }
    }).then(function(res){
      self.mysuggestions=res.data.mysuggestions;
      self.othersuggestions=res.data.othersuggestions;
      self.suggestions.append(res.data.mysuggestions);
      self.suggestions.append(res.data.othersuggestions);
    })

  },
  methods:{
    submitSuggestion: function(){
      //const self=this;

      console.log(this.value, this.subcatpk)
    }
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
