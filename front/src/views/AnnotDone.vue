
<template>
  <v-container fill-height>
    <v-row justify="center">
    <v-col style="text-align: center;">
      <v-card style="overflow-y: scroll; padding: 5% 0;">
        <v-card-title>Thank you for your participation!</v-card-title>
        <v-card-text style="line-height: 1.8; color:black; font-size: 105%;">
          Here, we ask you to a few questions to help us analyze the results and improve the task. <br/>
          <!--
          <v-form style="width: 640px; margin: 10px auto; text-align: left; font-size: 90%;">
            1. How would you rate the minimum level of confidence when you select "Exactly" rather than "Can be". (Enter a number between 0% and 100%)
            <v-text-field
              v-model="name"
              :counter="10"
              :rules="nameRules"
              label="Name"
              required
            ></v-text-field>
          </v-form>
          -->
          
          <iframe id='postsurvey' src="https://docs.google.com/forms/d/e/1FAIpQLSeXHhHy0xBhJRq3EVunZoxd4OwmX9PQrfC7V5ZPr2FEO9SsTQ/viewform?embedded=true" width="640" height="1043" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
          
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            @click="onSubmit"
            color="deep-purple accent-2"
            class="mr-4"
            style="margin-left: auto;"
          >
            I have submitted the form, please give me the code
          </v-btn>
          <v-spacer></v-spacer>
          
        </v-card-actions>
        <span v-if="showCode">
          <div>Code to enter in MTurk: <b style="color: blue">{{this.token}}</b></div>
          <div style="padding-bottom: 1%">Thanks again for the participation! If you haven't, make sure you submit the form above as well 🙏</div>
        </span>
      </v-card>
      <br>
    </v-col>
    </v-row>
  </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: 'AnnotDone',
  data() {
    return {
      showCode: false,
      token: '',
    }
  },
  mounted: function() {
    const self=this;
    setTimeout(() => {
        document.getElementById('postsurvey').onload=function(){
          self.activateButton=true;}
      }, 1000);
  },   
  methods: {
    gotoReview: function () {
      var doctype=this.$router.currentRoute.fullPath.split('/')[2];
      var self=this;
      
      axios.post(self.$store.state.server_url + "/api/save-as-regular/", {
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
          }).then(function () {
            self.$router.push('../../review/'+doctype);
          });

    },
    onSubmit: function() {
      const self=this;
      axios.post(self.$store.state.server_url + '/api/submit-survey/', {
        mturk_id: self.$store.state.mturk_id,
      }).then(function(res){
        self.token = res.data.token
        self.showCode = true
      });
    }
  }
}
</script>

<!--
<template>
  <v-container fill-height>
    <v-row justify="center">
    <v-col style="text-align: center;">
      <v-card>
        <v-card-text>
          <p>In the next phase, you will review items that you marked as 'N/A' or 'CAN BE'.</p>
          <p>All the deferred annotations with 'EXACTLY' labels are saved as regular annotations!</p> 
        </v-card-text>
         <v-btn
            @click="gotoReview()"
            color="deep-purple accent-2"
            class="mr-4"
            style="margin-left: auto;"
            large
          >
            Next
          </v-btn>
      </v-card>
      <br>
    </v-col>
    </v-row>
  </v-container>
</template>


<script>
import axios from "axios";

export default {
  name: 'AnnotDone',
  methods: {
    gotoReview: function () {
      var doctype=this.$router.currentRoute.fullPath.split('/')[2];
      var self=this;
      
      axios.post(self.$store.state.server_url + "/api/save-as-regular/", {
            //mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType,
          }).then(function () {
            self.$router.push('../../review/'+doctype);
          });

    },
  }
}
</script>
-->