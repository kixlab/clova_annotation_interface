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
            :items="items"
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

export default {
  name: "Suggestion",
  props: [subcatpk],
  data: () => ({
      items: [{'id': 1, 'suggestion': 'sug-menu'},{'id': 2, 'suggestion': 'sug-menu2'}],
      value: null,
    }),
  methods:{
    submitSuggestion: function(){
      console.log(this.value, this.props.subcatpk)
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
