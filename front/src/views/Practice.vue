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
          <template v-if="this.$router.currentRoute.fullPath.split('/')[2]=='receipt'"> 
          As the receipts are from Indonesia, here are translations for commonly occuring words: <br>
          <b>Bayar - Pay | Tunai - Cash | Kembali(an) - Change | Pajak - Tax | PB1 - tax code </b>
          </template>
          <template v-if="this.$router.currentRoute.fullPath.split('/')[2]=='event'"> 
          <div>
          There are bounding boxes that are drawn to the <b>background, watermark, or logos</b>.
          Make sure to annotate <b>all those boxes</b> as well.
          </div>
          </template>
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
import BoxSelectionStatus from '@/components/BoxSelectionStatus.vue'
import DeferredAnnotation from '@/components/DeferredAnnotation.vue'
import DeferredAnnotationStatus from '@/components/DeferredAnnotationStatus.vue'

import axios from 'axios'
import { mapActions} from 'vuex'

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
    ...mapActions(['setCurrOrder', 'setShowAnswer']),

    updateStatus(){
      const self=this;
      var doctype=self.$router.currentRoute.fullPath.split('/')[2];
      axios.get(self.$store.state.server_url+'/api/get-status/', {
        params: {
            mturk_id: self.$store.state.mturk_id,
            doctype: doctype
          }
        }).then(function (res) {
          self.$store.commit('update_status',res.data.status);
      })
    },
    onSubmit() {
      const self = this;
      var doctype=self.$router.currentRoute.fullPath.split('/')[2];
      axios.post(self.$store.state.server_url+'/api/practice-done/',{
            mturk_id: self.$store.state.mturk_id,
      }).then(function(res){
        console.log(res);
          self.$store.commit('set_assigned_images', res.data.assigned_images);
          self.$store.commit('set_start_image_no', res.data.assigned_images[0]);
          self.$store.commit('set_curr_image', 0);
          setTimeout(
            function(){
                  self.$router.push('/annotation/'+doctype+'/') }   ,500);
        })
      }
  },
  mounted(){
    this.updateStatus();
    this.setShowAnswer(false);
  },
  computed: {
    disabled() {
      return !this.$store.getters.getShowAnswer;
    }
  }
}
</script>
