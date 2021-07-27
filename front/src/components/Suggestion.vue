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
          <v-autocomplete
            v-model="value"
            :items="items"
            dense
          ></v-autocomplete>
        </v-col>
      </v-row>
  </v-container>
  <v-container fluid style='padding:0'>
      <v-row
      >
      <v-col cols='12' style='padding:0'>
          <v-btn
            x-small outlined
            color="primary" 
            class="close-btn">
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
  data: () => ({
      items: ['foo', 'bar', 'fizz', 'buzz'],
      values: ['foo', 'bar'],
      value: null,
    }),
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
