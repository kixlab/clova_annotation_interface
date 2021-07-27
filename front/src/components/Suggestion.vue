<template>
<v-card class='suggestion-holder'>
  <v-container fluid style='padding:0'>
      <v-row
      >
      <v-col cols='12' style='padding:0'>
          <v-btn
            x-small outlined
            color="error" 
            class="close-btn" v-on:click.stop="closeSuggestion">
            X
          </v-btn>
      </v-col>
      </v-row>
  </v-container>
  <v-container>
      <v-row>
        <v-col cols="12">
          
          <v-combobox
            v-model="select"
            :items="suggestions"
            :search-input.sync="search"
            dense
          >
          </v-combobox>
        </v-col>
      </v-row>
  </v-container>
  <v-container style='padding-bottom:20px;'>
          <v-btn
            x-small outlined
            color="primary" 
            class="close-btn" v-on:click.stop="markSuggestion">
            Suggest
          </v-btn>
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
      select: '',
      suggestions:[],
      search: null,
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
      var suggestions = res.data.mysuggestions.concat(res.data.othersuggestions)
      self.suggestions=suggestions;
     })

  },
  methods:{
    markSuggestion: function(){
      console.log(this.value)
      this.$emit('annotate', this.subcat, this.confidence, this.value);
      this.$emit('done');},
    closeSuggestion: function(){
      this.$emit('done');
    }
  }
};
</script>

<style scoped>
.close-btn{
  padding:5 !important;
  min-width: 0px !important;
  position: absolute;
  right: 10px;
}

.suggestion-holder{
  border: 1px solid grey;
}
</style>
