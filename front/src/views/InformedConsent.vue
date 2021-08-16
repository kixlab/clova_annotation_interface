<template>
  <v-row justify="center" align-content="center" align="center" class="instr" >
    <v-col cols="9" style="overflow-y: auto; border: 0px solid red; padding: 5% 0;">
      <h2> Informed Consent for Experiment </h2>
      <h3> </h3>
      1. This experiment is conducted for the sake of research only.<br><br>

      2. This research is to re-design the machine learning dataset generation process with crowdsourcing. <br><br>

      3. In this experiment, you will <b>assign appropriate labels to the text boxes</b> on <b>20 different receipt images</b>.<br><br>

      4. As the annotation interface to be used in this experiment does not include an invasive treatment, 
      you are informed that no side effects are known or expected. 
      However, you may experience unexpected risks by participating in the research.<br><br>

      5. Your private and personal information will be kept confidential and access to it by the general public will be restricted. 
      However, as long as the relevant law or regulation allows, your personal information can be made available to the review board and to governmental institutions with the aim of verifying the reliability of the experiment procedures and data. 
      However, even in such a case, the information will be kept in the strictest confidence. If the results of this research are published, your identity will remain confidential.<br><br>

      6. The final decision regarding whether or not to participate in this experiment is to be made by you. 
      You can always decide not to participate in the tasks and can withdraw your participation anytime. Even if you refuse to participate in this research, you will not be disadvantaged at all.<br><br>

      7. Contact Information<br>
      
      If you have any questions or wish to express any discomfort related to this research, please feel free to contact the researcher below. <br><br>
      <b>&lt;Name of researcher: Jeongeon Park, Contact: <a>jeongeonpark1@gmail.com</a>&gt; <br><br></b>

      <v-divider/> <br/>
      <h4>I have read this Informed Consent and received a response to each and every question asked. <br/>I hereby confirm that I would like to voluntarily participate in the research.<br><br></h4>

      <v-btn
        @click="onClickNext"
        color="deep-purple accent-2"
        class="mr-4 right_button"
        dark
      >
        Agree & Next
      </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";

export default {
  name: 'InformedConsent',
  methods: {
    onClickNext: function () {
      const self = this;
      axios.post(self.$store.state.server_url + '/api/consent-agreed/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( function(){
          self.$router.push('../instruction/')
        })  
      ;
    }
  },
  beforeCreate() {
    this.$helpers.isWrongAccess(this)
  }
}
</script>
<style scoped>
.instr {
  height: 100%;
  text-align: left;
}
</style>