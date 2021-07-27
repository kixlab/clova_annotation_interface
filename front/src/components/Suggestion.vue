<template>
<v-card>
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
  padding:0 !important;
  width: 20px;
  position: absolute;
  right: 0;
}
</style>
