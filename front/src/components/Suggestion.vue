<template>
  <v-card>
    <v-container fluid>
      <v-row
        align="center"
      >
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
</style>
