<template>
    <v-container fluid fill-height>
        <v-row align-content='center'>
            <v-col>
                <h2>Thank you for the annotations! We hope it was fun :)</h2> <br>
                <h3>In this page, we ask you to choose annotations <u>that represent similar suggestions</u>, <br/>
                and to fill out a <u>short survey</u> regarding the overall task.</h3>
            </v-col>
        </v-row>
        <v-row align-content='center' style="border: 0px solid red; height: 100%; overflow-y: auto">
            <v-col>
                <v-row>
                    <v-col>
                    <v-row>
                        <h2>Choose similar suggestions</h2>
                    </v-row>
                    <v-row style="height: 100%;">
                        <v-col cols="3" style="border: 1px solid black; ">
                            <!--<h3>Suggestions</h3>-->
                            <div>Please click on one of your suggestions!</div>
                            <h4 style="text-align: left; margin-top: 10px">Close To Suggestions</h4>
                            <div v-for="(v, idx) in unreviewed_issues.filter(v => v.suggestion_subcat !== 'n/a')" :key="'closeto-' + idx" style="overflow-y: scroll">
                                <v-btn depressed :outlined="v !== sel_issue" color="warning" small style="margin: 5px" @click="clickCloseto(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                x {{v.n_mine}}
                            </div>
                            <h4 style="text-align: left; margin-top: 10px">N/A Suggestions</h4>
                            <div v-for="(v, idx) in unreviewed_issues.filter(v => v.suggestion_subcat === 'n/a')" :key="'n/a-' + idx" style="overflow-y: scroll">
                                <v-btn depressed :outlined="v !== sel_issue" color="error" small style="margin: 5px" @click="clickNa(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                x {{v.n_mine}}
                            </div>
                        </v-col>
                        <v-col cols="3" style="border: 1px solid black; ">
                            <h3>Corresponding annotations</h3>
                            <v-row style="height: 400px; overflow-y: auto; border: 0px solid lightgray; margin: 10px 3px 0; background-color: #eeeeee;">
                                <div v-for="(annot, idx) in sel_issue.mine" :key="idx" >
                                    <v-img :src="imageNo2Url(annot.image_no)" width="250">
                                    </v-img>
                                    <div style="text-align: left; margin-bottom: 5px;">Reason: <b>{{annot.reason}}</b></div>
                                </div>
                            </v-row>
                        </v-col>
                        <v-col cols="6" style="border: 1px solid black; ">
                            <h3>Similar suggestions ({{sel_issue.others.length}} total)</h3>
                            <v-row style="height: 400px; overflow-y: auto; border: 0px solid lightgray; margin: 10px 3px 0; background-color: #eeeeee;">
                                <v-col v-for="(annot, idx) in sel_issue.others" :key="idx" >
                                    <v-checkbox hide-details style="margin: 0;" v-model="sel_sim_issues" :label="'Suggestion from Image #'+annot.image_no" :value="annot"/>
                                    <v-img :src="imageNo2Url(annot.image_no)" width="250" @click="selectIssues(annot)" :style="'border: '+sel_sim_issues.indexOf(annot) > -1 ? 1 : 0+'px solid black;'">
                                    </v-img>
                                    <div style="text-align: left; margin-bottom: 5px;">Reason: <b>{{annot.reason}}</b></div>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>
                    </v-col>
                </v-row>
                <v-row style="height: 20px; border: 0px solid orange"></v-row>
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
            sel_issue: {
                mine:[],
                otehrs: []
            },

            sel_sim_issues: [],

            unreviewed_issues: [],
            issues_with_suggestions:[],




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

        axios.get(self.$store.state.server_url + "/api/get-random-suggestions-to-review/",{
        params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType
        }
        }).then(function(res){
            self.issues_with_suggestions=res.data.suggestions;
            console.log("Hi", self.issues_with_suggestions)
        })

        axios.get(self.$store.state.server_url + "/api/get-unreviewed-issues/",{
        params:{
            mturk_id: self.$store.state.mturk_id,
            doctype: self.$route.params.docType
        }
        }).then(function(res){
            self.unreviewed_issues=res.data.unreviewed_issues;
            console.log(self.unreviewed_issues)
        })


        // get annotation 단위 --> image id, box id(s), suggestion
    },

    methods: {
        validate () {
            this.$refs.form.validate()
        },
        groupIssues(my_issue_pks, other_issue_pks){
            // my_issues_pks: [1,2,3,4,5]
            // other_issues_pks: [10,11,12,13] 
            // e.g.,       self.groupIssues([349], [326]) 형태로 사용하시면 됩니다! 
            const self=this;
            axios.post(self.$store.state.server_url + "/api/save-grouped-issues/", {
                doctype: self.$route.params.docType,
                mturk_id: self.$store.state.mturk_id,
                my_issue_pks: my_issue_pks,
                other_issue_pks: other_issue_pks
            }).then(function (res) { // get issue list again 
                self.unreviewed_issues=res.data.unreviewed_issues;
            });
        },

        selectIssues(annot) {
            if (this.sel_sim_issues.indexOf(annot) > -1) {
                this.sel_sim_issues.splice(this.sel_sim_issues.indexOf(annot), 1)
            } else {
                this.sel_sim_issues.push(annot)
            }
            //console.log(annot)
            //console.log(this.sel_sim_issues.length)
        },


        clickCloseto(sugg) {
            console.log(sugg)
            this.sel_issue = sugg
        },

        clickNa(sugg) {
            console.log(sugg)
            this.sel_issue = sugg
        },


        // Rendering 관련 함수들
        setImageBoxes(json) {
            //console.log("NEW JSON --------\n" , json)
            const img_w = json[0].meta === undefined ? json[0].image_size.width : (json[0].meta.image_size === undefined? json[0].meta.imageSize.width:json[0].meta.image_size.width)
            const img_h = json[0].meta === undefined ? json[0].image_size.height : (json[0].meta.image_size === undefined? json[0].meta.imageSize.height:json[0].meta.image_size.height)
            var ratio = 1
            var padding_x = 0
            var padding_y = 0
            if (img_w/json[1] >= img_h/json[2]) {
                ratio = img_w/json[1]
                padding_y = 0//(json[2]-(img_h/ratio))/2
            } else {
                ratio = img_h/json[2]
                padding_x = (json[1]-(img_w/ratio))/2
            }

            //commit('setImageRatio', ratio)
            
            const validData=json[0].valid_line.map(v => v.words).flat(1)

            //const newValidData = []
            for (var d in json[0].valid_line) {
                var word = json[0].valid_line[d].words
                var cat = json[0].valid_line[d].category
                for (var w in word) {
                    word[w]["GTlabel"] = cat
                    //newValidData.push(word[w])
                }
            }
            //console.log("VALIDDATA", validData)
            const processedData = validData.map(function(i, idx) {
                return {box_id: idx,
                        text: i.text,
                        x_pos: i.quad.x1/ratio+padding_x, 
                        y_pos: i.quad.y1/ratio+padding_y, 
                        x_len: (i.quad.x2-i.quad.x1)/ratio, 
                        y_len: (i.quad.y3-i.quad.y2)/ratio, 
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.quad.x1, y1: i.quad.y1, x2: i.quad.x2, y2: i.quad.y2, y3: i.quad.y3},
                        label: "",
                        GTlabel: i.GTlabel,
                    }
            })
            return processedData
        },

        imageNo2Url(no) {
            var docType= 'receipt'
            var three_digit_id = ("00" + no).slice(-3);
            return this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
        },

        imageNo2Json(no, box_id, annot) {
            const self = this;
            var docType= 'receipt'
            var three_digit_id = ("00" + no).slice(-3);
            const json_url = this.$store.state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
            
            return axios.get(json_url).then(function(res) {
                var json = res.data;
                var img_width = json.meta === undefined ? json.image_size.width:(json.meta.image_size === undefined? json.meta.imageSize.width:json.meta.image_size.width)
                var img_height = json.meta === undefined ? json.image_size.height:(json.meta.image_size === undefined? json.meta.imageSize.height:json.meta.image_size.height)

                const width = 250;//cont_pos.right-cont_pos.left
                //const height = cont_pos.bottom-cont_pos.top

                const resbox = self.setImageBoxes([json, width, width*img_height/img_width, true]);
                //self.original_box = json;

                //console.log(resbox)
                //self.$forceUpdate();
                self.done = ''
                //console.log(box_id)
                var texts = []
                if (resbox && box_id) {
                    for (var b in resbox) {
                        if (box_id.indexOf(resbox[b].box_id) > -1) {
                            //console.log(resbox[b].text)
                            texts.push(resbox[b].text)
                        }
                    }
                }
                if (annot) {
                    annot.boxes_text = texts
                }


                return resbox
            })
        },
    },

}
</script>

<style scoped>

</style>