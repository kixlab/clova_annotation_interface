<template>
<v-container>
  <v-row justify="center" align-content="center" align="center" class="up_margin">
    <div style="width: 80%;">
    <h1> Welcome! </h1>
    Thank you for your participation!<br><br>

    This task is conducted as a part of a research project in which we try to re-design the machine learning dataset generation process with crowdsourcing. 
    In this task, you will be asked to label text boxes on a event flyer image with a given label set.<br>

    <br><v-divider/><br>

    <h3 style="color:red;"> CAUTIONS </h3>
    <ul>
      <!--<li> <b>An MTurk user can participate in this task <span style="color:red">only once</span>.</b> </li>-->
      <li> <b>This is the version 2 task.</b> You can participate on this <b>task multiple times (through multiple HITs)</b>, but cannot participate on a different version task.</li>
      <li> This task is expected to take 70 minutes at maximum.</li>
      <li> You will be provided with a token after completing the task. You <b>MUST</b> submit this token to the Amazon MTurk website to get rewards. </li>
      <li> If majority of your annotations are found to not follow the instructions, you may not be rewarded.</li>
      <li> It is strongly recommended that you use <a target="_blank" rel="noopener noreferrer" href="https://www.google.com/chrome/">chrome</a> browser in your desktop/laptop for the task. 
      Other browsers or mobile devices may show unexpected behaviors.</li>
    </ul>
    <br>

    <h3> STEPS </h3>
    <ol>
      <li> Read the informed consent and agree to participate </li>
      <li> Read the instruction </li>
      <li> Practice session with eventy flyer image </li>
      <li> Annotate 20 event flyer images </li>
      <li> Review your annotation </li>
      <li> Do a simple survey and submit a token to Amazon MTurk webpage</li>
    </ol>
    <br>

    <v-img :src="require('@/assets/overview.png')">
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
import { mapState, mapActions } from "vuex";
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
    ...mapActions(['setServerURL']),
    checkUser: function (){
      const self=this;
    axios.post('http://15.165.236.102:8000/api/check-proposed-user/', {
      mturk_id: self.$store.state.mturk_id,
    }).then( function(res){
      if(res.data.is_new){
        self.$router.push('../informed-consent/')   
      }
      else{
        window.alert('It seems that you have participated in the version 1 task. Please look for HITs with *version 1* and participate. If you have any other questions, please contact jeongeonpark1@gmail.com.')
      }
      })
  },
    onClickNext: function () {
      const self = this;
      self.$refs.form.validate()
      self.$store.commit('set_mturk_id', self.turk_id.trim())
      self.checkUser()
      axios.post('http://3.38.105.16:8000' + '/api/signup/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( (res)=>{
        console.log(res)
      });
      axios.post('http://52.78.121.66:8000' + '/api/signup/', {
        mturk_id: self.$store.state.mturk_id,
      }).then( (res)=>{
        self.$store.commit('set_mturk_id', res.data.username)
        console.log(res.data)
        
        if(res.data.step=='new'){ //http://15.165.236.102:8000
          self.$store.commit('update_status', new Array(21).fill(false));
          self.checkUser();          
        }
        if(res.data.step=='consent'){
          self.checkUser(); 
        }
        if(res.data.step=='instruction'){
          self.$router.push('/instruction/'+res.data.doctype)
        }
        if(res.data.step=='annotation'){
          self.$router.push('/annotation/'+res.data.doctype)
        }
        
      });
    }
  },
  
  mounted() {
    this.turk_id = this.mturk_id;
    this.setServerURL('http://52.78.121.66:8000')
  }
}
</script>

<style scoped>
.up_margin {
  margin-top:2rem;
  text-align: left;
}
</style>
