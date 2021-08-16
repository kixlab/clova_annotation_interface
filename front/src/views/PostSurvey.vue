<template>
<div>
  <v-row justify="center" align-content="center" align="center" class="instr" >
    <v-col cols="9" style="overflow-y: auto; border: 0px solid red; padding: 5% 0;">
      <iframe id='postsurvey' src="https://docs.google.com/forms/d/e/1FAIpQLScYKocOokiB-6D5KRn6k3TSxfjoXb1t8x0Tfi8fF252zfvtfQ/viewform?embedded=true" width="640" height="1043" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
    </v-col>
    <v-col v-if="showCode"  cols="3" style="overflow-y: auto; border: 0px solid red; padding: 5% 0;">
      <span v-if="showCode">
          <div style="margin-top: 10px; ">Code to enter in MTurk: <b style="color: blue">{{this.token}}</b></div>
          <div style="padding-bottom: 1%">Thanks again for the participation!</div>
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
        });        }
      }, 1000);
  },     
/*   methods: {
  onSubmit: function() {
        const self=this;
        console.log(this.q1, this.q2, this.q3, this.q4) // 보내게 될 4가지 질문에 대한 답이 여기에 저장되어있어요!
        axios.post(self.$store.state.server_url + '/api/submit-survey/', {
            mturk_id: self.$store.state.mturk_id,
            // 여기에 survey detail들 넣고 싶다!
        }).then(function(res){
            self.token = res.data.token
            self.showCode = true
        });
    }
      }, */
}
</script>
<style scoped>
.instr {
  height: 100%;
  text-align: left;
}
</style>