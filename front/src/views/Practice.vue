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
      <v-btn
        :disabled="disabled"
        color="normal"
        @click="onSubmit"
      >
        Proceed
        <v-icon right>
          mdi-arrow-right
        </v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
        <v-row dense>
          <b style="color:red; margin-right: 8px;">* Important * </b>  This is a part of the tutorial where you can check your understanding with the requester's provided answer. Please practice with the provided image.
        </v-row>
        <v-row dense style="margin-top: 10px;"> 
          Also, the receipts are from Indonesia, here are translations for commonly occuring words: <br>
          <b>Bayar - Pay | Tunai - Cash | Kembali(an) - Change | Pajak - Tax | PB1 - tax code </b>
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
              <practice-deferred-annotation/>
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
import PracticeDeferredAnnotation from '@/components/PracticeDeferredAnnotation.vue'
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
    PracticeDeferredAnnotation,
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
    },
    onSubmit() {
      const self = this;

      axios.post(self.$store.state.server_url+'/api/instr-done/',{
            mturk_id: self.$store.state.mturk_id,
            doctype: 'receipt'
      }).then(function(res){
          self.$store.commit('set_assigned_images', res.data.assigned_images);
          self.$store.commit('set_start_image_no', res.data.assigned_images[0]);
          self.$store.commit('set_curr_image', 0);
          setTimeout(
                  self.$router.push('/annotation/'+res.data.doctype)    ,500);
        })
      }
  },
  mounted(){
    this.updateStatus();
  },
  computed: {
    disabled() {
      return !this.$store.getters.getShowAnswer;
    }
  }
}
</script>
