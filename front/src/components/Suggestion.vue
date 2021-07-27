<template>
    <v-container fluid>
      <v-row
      >
      <v-btn
        small 
        color="error" 
        depressed 
        class="close-btn">
        X
      </v-btn>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-autocomplete
            v-model="value"
            :items="items"
            dense
            filled
            label="Filled"
          ></v-autocomplete>
        </v-col>
      </v-row>
    </v-container>
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
  padding:0 !important
}
</style>
