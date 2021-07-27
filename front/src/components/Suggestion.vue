<template>
<v-card class='suggestion-holder'>
      <v-row
      >
      <v-btn
        x-small outlined
        color="error" 
        class="close-btn">
        X
      </v-btn>
      </v-row>
      <v-row>
        <v-col cols="9">
          <v-autocomplete
            v-model="value"
            :items="items"
            dense
          ></v-autocomplete>
        </v-col>
        <v-col cols="3">
          <v-btn
            x-small outlined
            color="primary" 
            class="suggestion-btn">
            Suggest
          </v-btn>
        </v-col>
      </v-row>
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
