<template>
    <v-container fluid fill-height>
        <v-row align-content='center'>
            <v-col>
                <h2>Thank you for the annotations! We hope it was fun :)</h2> <br>
                <h3>In this page, we ask you to <u>choose similar issues to your issue</u>, <br/>
                and to fill out a <u>short survey</u> regarding the overall task.</h3>
            </v-col>
        </v-row>
        <v-row align-content='center' style="border: 0px solid red; min-height: 60vh; max-height: 75vh">
            <v-col>
                <v-row>
                    <v-col>
                    <v-row>
                        <h2>Choose similar issues</h2>
                    </v-row>
                    <v-row style="min-height: 45vh;">
                        <v-col cols="3" style="border: 1px solid black; ">
                            <h3>Issues</h3>
                            <div v-for="(v, idx) in issue_list" :key="idx" style="overflow-y: scroll">
                                <v-btn depressed color="primary" small style="margin: 5px"> {{v.suggestion_cat}}-{{v.suggestion_subcat}}-{{v.suggestion_text}} </v-btn>
                            </div>
                        </v-col>
                        <v-col cols="3" style="border: 1px solid black; ">
                            <h3>Specific boxes</h3>
                            <v-img :src="'http://13.125.191.49:8000/media/receipt/receipt_00300.png'" width="250">
                            </v-img>
                            <div>Reason:</div>
                        </v-col>
                        <v-col cols="6" style="border: 1px solid black; ">
                            <h3>Similar issues</h3>
                        </v-col>
                    </v-row>
                    </v-col>
                </v-row>
                <v-row style="height: 20px"></v-row>
                <v-row>
                    <h2>Post-survey</h2>
                    <div style="border: 1px solid black; ">
                            <v-form ref='form' v-model='valid' lazy-validation>
                                <v-text-field
                                v-model="name"
                                :counter="10"
                                :rules="nameRules"
                                label="Name"
                                required
                                ></v-text-field>
                            When did you decide to use the *close to* button to annotate? Why? *
                            When did you decide to use the *n/a* button to annotate? Why? *
                            Tell us the *overall confidence* in your annotation (Enter a number between 0% and 100%) *
                            Do you have any additional questions, suggestions, or feedback regarding the task?
                            </v-form>

                            <v-btn
                            :disabled="!valid"
                            color="success"
                            class="mr-4"
                            @click="validate"
                            >
                            Validate
                            </v-btn>
                    </div>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";

export default {
    name: 'ReviewSuggestion',
    data () {
        return {
            issue_list: [],





            // Related to the survey
            valid: true,
            name: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],





        }
    },

    mounted: function() {
        const self=this;

    axios.get(self.$store.state.server_url + "/api/get-suggestions-to-review/",{
      params:{
        mturk_id: self.$store.state.mturk_id,
        doctype: self.$route.params.docType
      }
    }).then(function(res){
        console.log('init', res.data);
        self.issue_list=res.data.suggestions;
    })

    setTimeout( function(){
        console.log("group");
      self.groupIssues([349], [326]);
      }
    ,5000);

        // get annotation 단위 --> image id, box id(s), suggestion
    },

    methods: {
        validate () {
            this.$refs.form.validate()
        },
        groupIssues(my_issue_pks, other_issue_pks){
            // my_issues_pks: [1,2,3,4,5]
            // other_issues_pks: [10,11,12,13] 
            const self=this;
            axios.post(self.$store.state.server_url + "/api/save-grouped-issues/", {
                doctype: self.$route.params.docType,
                mturk_id: self.$store.state.mturk_id,
                my_issue_pks: my_issue_pks,
                other_issue_pks: other_issue_pks
            }).then(function (res) { // get issue list again 
                self.issue_list=res.data.suggestions;
                console.log(res.data)
            });
      }
    },

}
</script>

<style scoped>

</style>