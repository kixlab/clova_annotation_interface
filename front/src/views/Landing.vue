<template>
<v-container>
  <v-row justify="center" align-content="center" align="center" class="up_margin">
    <div style="width: 80%;">
    <h1> Welcome! </h1>
    Thank you for your participation!<br><br>

    This task is conducted as a part of a research project in which we try to re-design the machine learning dataset generation process with crowdsourcing. 
    In this task, you will be asked to label text boxes on a receipt image with a given label set.<br>

    <br><v-divider/><br>

    <h3 style="color:red;"> CAUTIONS </h3>
    <ul>
      <li> <b>An MTurk user can participate in this task only once.</b> </li>
      <li> This task is expected to take 60 minutes at maximum.</li>
      <li> You will be provided with a token after completing the task. You <b>MUST</b> submit this token to the Amazon MTurk website to get rewards. </li>
      <li> If majority of your annotations are found to not follow the instructions, you may not be rewarded.</li>
      <li> It is strongly recommended that you use <a target="_blank" rel="noopener noreferrer" href="https://www.google.com/chrome/">chrome</a> browser in your desktop/laptop for the task. 
      Other browsers or mobile devices may show unexpected behaviors.</li>
    </ul>
    <br>

    <h3> STEPS </h3>
    <ol>
      <li> Read instruction </li>
      <li> Practice session with one receipt image </li>
      <li> Annotate 20 receipt images </li>
      <li> Do a simple survey and submit a token to Amazon MTurk webpage</li>
    </ol>
    <br>

    <v-img src="require('@/assets/overview.png')">
        </v-img>
    <h4>For any questions, please contact : <a>jeongeonpark1@gmail.com</a> </h4> <br/>
    <h4>Fill in the blank with your MTurk ID and click the button below to proceed to the next step.</h4>
    <v-form
      ref="form"
      v-model="valid"
      style="width:40%;"
    >
    <v-text-field
      v-model="turk_id"
      :rules="idRules"
      label="MTurk ID"
      required
    ></v-text-field>
    </v-form>
  <v-divider/>
    </div>
  </v-row>

  <v-row justify="space-around" align="start" class="up_margin">
    <v-btn
      :disabled="!valid"
      @click="onClickNext"
      
      color="indigo lighten-1"
      class="mr-4"
    >
      Next
    </v-btn>
  </v-row>
</v-container>
</template>


<script>
// @ is an alias to /src
import { mapState } from "vuex";
import axios from 'axios';

export default {
  name: 'Landing',
  data: () => ({
    valid: true,
    turk_id: '',
    idRules: [
      v => !!v || 'MTurk ID is required',
    ]
  }),
  computed: {
    ...mapState(['mturk_id'])
  },
  methods: {
    onClickNext: function () {
      const self = this;
      self.$refs.form.validate()
      self.$store.commit('set_mturk_id', self.turk_id.trim())
      axios.post(self.$store.state.server_url + '/api/signup/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( function(res){
//        self.$store.commit('set_mturk_id', self.turk_id.trim())
        if(res.data.step=='new'){
           self.$store.commit('update_status', new Array(21).fill(false));
          self.$router.push('../informed-consent/')   
        }
        if(res.data.step=='consent'){
           self.$router.push('../informed-consent/')   
        }
        if(res.data.step=='instruction'){
          self.$router.push('/instruction/')
        }
        if(res.data.status=='annotation'){
          self.$router.push('/annotation/'+res.data.doctype)
        }
      });
    }
  },
  mounted() {
    this.turk_id = this.mturk_id;
  }
}
</script>

<style scoped>
.up_margin {
  margin-top:2rem;
  text-align: left;
}
</style>
