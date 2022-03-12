<template>
<div>
  <v-row justify="center" align-content="center" align="center" class="instr" >
    <v-col cols="8" style="overflow-y: auto; border: 0px solid red; padding: 5% 0;">
      <iframe id='postsurvey' src="https://docs.google.com/forms/d/e/1FAIpQLSeXHhHy0xBhJRq3EVunZoxd4OwmX9PQrfC7V5ZPr2FEO9SsTQ/viewform?embedded=true" width="640" height="1043" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    </v-col>
    <v-col cols="4" style="overflow-y: auto; border: 0px solid red; position: absolute; top:50px; right: 0px;">
      <span v-if="showCode">
          <div style="margin-top: 10px; font-size: large ">Code to enter in MTurk: </div>
          <div><b style="color: blue; font-size: xx-large">{{this.token}}</b></div>
          <div style="padding-bottom: 1%; font-size: large ">Thanks again for the participation!</div>
      </span>
    </v-col>
  </v-row>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'PostSurvey',
  data () {
        return {
            showCode: false,
            token: '',
        }
    },
  mounted: function() {
    const self=this;
    setTimeout(() => {
        document.getElementById('postsurvey').onload=function(){
        axios.post(self.$store.state.server_url + '/api/submit-survey/', {
            mturk_id: self.$store.state.mturk_id,
        }).then(function(res){
          console.log('submitted')
            self.token = res.data.token
            self.showCode = true
            window.scrollTo({top:0});
        });        }
      }, 1000);
  },     
}
</script>
<style scoped>
.instr {
  height: 100%;
  text-align: left;
}
</style>