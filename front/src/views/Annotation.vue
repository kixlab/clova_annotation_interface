<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo lighten-1"
      dark
      dense
      fixed
    >
      <v-toolbar-title>Image Annotation (ID: {{this.$store.state.mturk_id}}, {{this.$store.state.image_order+1}} of 20 images)</v-toolbar-title>
      <v-spacer/>
      <annotation-instruction-button/>
      <submit-button/>
    </v-app-bar>

    <v-main>
      <v-container fluid fill-height>
        <v-row> 
          <Progress/>
        </v-row>
        <v-row dense style="margin-top: 15px;"> 
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
            <image-panel/>
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
import ImagePanel from '@/components/ImagePanel.vue'
import DeferredAnnotationStatus from '@/components/DeferredAnnotationStatus.vue'
import SubmitButton from '@/components/SubmitButton.vue'
import AnnotationInstructionButton from '@/components/AnnotationInstructionButton.vue'
//import OverviewButton from '@/components/OverviewButton.vue'
import DeferredAnnotation from '@/components/DeferredAnnotation.vue'
import BoxSelectionStatus from '@/components/BoxSelectionStatus.vue'
import Progress from '@/components/Progress.vue'
import axios from 'axios'
//import SubmitButton from '../components/SubmitButton.vue'

export default {
  name: 'Home',
  components: {
    Progress,
    ImagePanel,
    DeferredAnnotationStatus,
    SubmitButton,
    AnnotationInstructionButton,
  //  OverviewButton,
    DeferredAnnotation,
    BoxSelectionStatus,
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
            doctype: self.$route.params.docType
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
