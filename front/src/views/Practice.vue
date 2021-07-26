<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo lighten-1"
      dark
      dense
      fixed
    >
      <v-toolbar-title>Practice Annotation (ID: {{this.$store.state.mturk_id}})</v-toolbar-title>
      <v-spacer/>
      <practice-instruction-button />
      <practice-submit-button/>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
        <v-row dense>
          <b style="color:red; margin-right: 8px;">* Important * </b>  This is a part of the tutorial where you can check your understanding with the requester's provided answer. Please practice with the provided image.
        </v-row>
        <v-row align-content="start">
          <!-- COL1 - IMAGE LOADER -->
          <v-col cols="5">
            <v-row dense>
              <practice-image-panel/>
            </v-row>
          </v-col>

          <!-- COL2 - ANNOTATION UI -->
          <v-col cols="7">
            <v-row dense>
              <box-selection-status/>
              <deferred-annotation/>
              <deferred-annotation-status/>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>

</template>

<script>
// @ is an alias to /src
import PracticeImagePanel from '@/components/PracticeImagePanel.vue'
import PracticeSubmitButton from '@/components/PracticeSubmitButton.vue'

import PracticeInstructionButton from '@/components/PracticeInstructionButton.vue'
//import OverviewButton from '@/components/OverviewButton.vue'

import BoxSelectionStatus from '@/components/BoxSelectionStatus.vue'
import DeferredAnnotation from '@/components/DeferredAnnotation.vue'
import DeferredAnnotationStatus from '@/components/DeferredAnnotationStatus.vue'


import axios from 'axios'
//import SubmitButton from '../components/SubmitButton.vue'

export default {
  name: 'Home',
  components: {
    PracticeImagePanel,
    PracticeSubmitButton,
    PracticeInstructionButton,
  //  OverviewButton,
    
    BoxSelectionStatus,
    DeferredAnnotation,
    DeferredAnnotationStatus,
    
  },
  beforeCreate() {
    this.$helpers.isWrongAccess(this)

  },
  methods:{
    updateStatus(){
      const self=this;
      axios.get(self.$store.state.server_url+'/api/get-status/', {
        params: {
            mturk_id: self.$store.state.mturk_id,
            doctype: 'receipt'
          }
        }).then(function (res) {
          self.$store.commit('update_status',res.data.status);
      })
    }
  },
  mounted(){
    this.updateStatus();
  }
}
</script>
