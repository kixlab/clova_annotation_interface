<template>
  <v-tooltip bottom :disabled="!disabled">
    <template v-slot:activator="{ on, attrs }">
      <div v-on="on">
      <v-btn
        class="ma-2"
        :disabled="disabled"
        color="error"
        @click="onSubmit"
        v-bind="attrs"
        v-on="on"
      >
        Next
      </v-btn>
      </div>
    </template>
    Annotate all the images to submit!
  </v-tooltip>
</template>

<script>
import axios from "axios";
import {mapGetters} from 'vuex';

export default {
  name: "SubmitButton",
  methods: {
    ...mapGetters(['getIfAllImagesAnnotated']),

    onSubmit: function() {
      const self=this;
      axios.post(self.$store.state.server_url + '/api/annotation-done/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( function(){
        const doctype=self.$route.params.docType
        self.$router.push('../../review-suggestion/'+doctype+'/');
      });

      
 }
  },

  computed: {
    disabled() {
      return !this.$store.getters.getIfAllImagesAnnotated
    }
  }
}
</script>
