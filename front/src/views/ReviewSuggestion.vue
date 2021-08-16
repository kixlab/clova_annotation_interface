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
                            <div v-for="(v, idx) in issues_with_suggestions.filter(v => v.suggestion_subcat !== 'n/a')" :key="'closeto-' + idx" style="overflow-y: scroll">
                                <v-btn depressed :outlined="v.suggestion_pk !== sel_issue.suggestion_pk" color="warning" small style="margin: 5px" @click="clickCloseto(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                x {{v.n_issues}}
                            </div>
                            <h4 style="text-align: left; margin-top: 10px">N/A Suggestions</h4>
                            <div v-for="(v, idx) in issues_with_suggestions.filter(v => v.suggestion_subcat === 'n/a')" :key="'n/a-' + idx" style="overflow-y: scroll">
                                <v-btn depressed :outlined="v.suggestion_pk !== sel_issue.suggestion_pk" color="error" small style="margin: 5px" @click="clickNa(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                x {{v.n_issues}}
                            </div>
                        </v-col>
                        <v-col cols="3" style="border: 1px solid black; ">
                            <h3>Corresponding annotations</h3>
                            <v-row style="height: 400px; overflow-y: auto; border: 0px solid lightgray; margin: 10px 3px 0; background-color: #eeeeee;">
                                <div v-for="(annot, idx) in sel_issue.mine" :key="idx" >
                                    <v-img :src="imageNo2Url(annot.image_no)" width="250">
                                        <div v-if="annot_boxes[annot.issue_pk]">
                                            <div style="margin: 0; background: gray; color: white; font-size: 90%">{{annot_boxes[annot.issue_pk].map(v=>v.text)}}</div>
                                            <div v-for="box in annot_boxes[annot.issue_pk]" :key="box.id"><!--{{annot_boxes[annot.issue_pk].length}}-->
                                                <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                                            </div>
                                        </div>
                                        <div style="opacity: 0.0;">{{waitForJson(annot.image_no, annot.boxes_id, annot.issue_pk)}}</div>
                                    </v-img>
                                    <div style="text-align: left; margin-bottom: 5px;">Reason: <b>{{annot.reason}}</b></div>
                                </div>
                            </v-row>
                        </v-col>
                        <v-col cols="6" style="border: 1px solid black; ">
                            <h3>Similar suggestions ({{sel_issue.others.length}} total)</h3>
                            <v-row style="height: 400px; overflow-y: auto; border: 0px solid lightgray; margin: 10px 3px 0; background-color: #eeeeee;">
                                <v-col cols="auto" v-for="(annot, idx) in sel_issue.others" :key="idx" style="border: 1px solid black">
                                    <!--<v-checkbox hide-details style="margin: 0;" v-model="sel_sim_issues" :label="''+(idx+1)+'. Suggestion from Image #'+annot.image_no" :value="annot"/>-->
                                    <div style="text-align: left; ">{{idx+1}}. Suggestion from image #{{annot.image_no}}</div>
                                    <v-img :src="imageNo2Url(annot.image_no)" width="250" @click="selectIssues(annot)" :style="'border: '+sel_sim_issues.indexOf(annot) > -1 ? 1 : 0+'px solid black;'">
                                        <div v-if="annot_boxes[annot.issue_pk]">
                                            <div style="margin: 0; background: gray; color: white; font-size: 90%">{{annot_boxes[annot.issue_pk].map(v=>v.text)}}</div>
                                            <div v-for="box in annot_boxes[annot.issue_pk]" :key="box.id"><!--{{annot_boxes[annot.issue_pk].length}}-->
                                                <bounding-box circle="no" color="stroke:red; fill:red; fill-opacity:0.1;" :box_info="box"/>
                                            </div>
                                        </div>
                                        <div style="opacity: 0.0;">{{waitForJson(annot.image_no, annot.boxes_id, annot.issue_pk)}}</div>
                                    </v-img>
                                    <div style="text-align: left; margin-bottom: 5px;">Reason: <b>{{annot.reason}}</b></div>
                                    <v-btn x-small depressed color="success" style="margin-right: 5px;" @click="similar(annot)">Similar</v-btn>
                                    <v-btn x-small depressed color="error" style="margin-left: 5px;" @click="notsimilar(annot)">Not similar</v-btn>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>
                    </v-col>
                </v-row>
                <v-row style="height: 20px; border: 0px solid orange"></v-row>
                <v-row>
                    <h2 style="width: 100%; text-align: left">Post-survey</h2>
                    <div style="border: 1px solid black; text-align: left; width: 100%;">
                        <v-form ref='form' v-model='valid' style="padding: 10px 2%">
                            
                            <v-text-field v-model="q1" counter :rules="q1Rules" 
                            label="Q1. When did you decide to use the *close to* button to annotate? Why?" required />
                            
                            <v-text-field v-model="q2" counter :rules="q1Rules" 
                            label="Q2. When did you decide to use the *n/a* button to annotate? Why?" required />

                            <v-text-field v-model="q3" counter :rules="q1Rules" 
                            label="Q3. Tell us the *overall confidence* in your annotation (Enter a number between 0% and 100%)" required />

                            <v-text-field v-model="q4" counter
                            label="Q4. Do you have any additional questions, suggestions, or feedback regarding the task?" />
                        
                            <v-btn :disabled="!valid_actual" color="success" class="mr-4" @click="submit">
                                Submit and get the code
                            </v-btn>
                            <v-btn color="error" class="mr-4" @click="reset">
                                Reset Form
                            </v-btn>
                            <span v-if="showCode">
                                <div style="margin-top: 10px; ">Code to enter in MTurk: <b style="color: blue">{{this.token}}</b></div>
                                <div style="padding-bottom: 1%">Thanks again for the participation!</div>
                            </span>

                        </v-form>
                    </div>
                </v-row>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import axios from "axios";
import BoundingBox from '@/components/BoundingBox.vue'
import {mapGetters} from 'vuex';

export default {
    name: 'ReviewSuggestion',
    components: {
        BoundingBox,
    },
    data () {
        return {
            issue_list: [],
            sel_issue: {
                mine:[],
                others: []
            },

            sel_sim_issues: [],

            unreviewed_issues: [], // 내가 한 suggestion 단위로 없어짐
            issues_with_suggestions:[], // 처음에 mount 함




            // Related to the survey
            valid: true,
            name: '',
            nameRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],

            q1: '',
            q2: '',
            q3: '',
            q4: '',
            q1Rules: [
                v => !!v || 'Answer cannot be empty',
                v => (v && v.length >= 5) || 'Answer must be more than 5 characters',
            ],
            
            showCode: false,
            token: '',

            annot_boxes: {},

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
            self.unreviewed_issues=res.data.suggestions.filter(v => v.others.length>0)
        })
    },

    methods: {
        submit () {
            this.$refs.form.validate()
            
            this.onSubmit()
        },
        reset () {
            this.$refs.form.reset()
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
            const sugg_pk=sugg.suggestion_pk
            this.sel_issue = this.issues_with_suggestions.filter(v => v.suggestion_pk == sugg_pk)[0]
        },

        clickNa(sugg) {
            const sugg_pk=sugg.suggestion_pk
            this.sel_issue = this.issues_with_suggestions.filter(v => v.suggestion_pk == sugg_pk)[0]
        },

        similar(annot) {
            const self = this
            const mine = self.sel_issue.mine.map(v => v.issue_pk)
            const others = annot.issue_pk

            axios.post(self.$store.state.server_url + "/api/save-similarity/", {
                doctype: self.$route.params.docType,
                mturk_id: self.$store.state.mturk_id,
                suggestion_pk: self.sel_issue.suggestion_pk,
                my_issue_pks: mine,
                other_issue_pk: others,
                similarity: true
            }).then(function (res) { // get issue list again 
                console.log(res)
                if(res.result){
                    const new_others = self.sel_issue.others
                    new_others.splice(new_others.indexOf(annot), 1)
                    self.unreviewed_issues=res.data.suggestions.filter(v => v.others.length>0)
                }
            });


        },

        notsimilar(annot) {
            //console.log(annot)
            const self = this
            const mine = self.sel_issue.mine.map(v => v.issue_pk)
            const others = annot.issue_pk

            axios.post(self.$store.state.server_url + "/api/save-similarity/", {
                doctype: self.$route.params.docType,
                mturk_id: self.$store.state.mturk_id,
                suggestion_pk: self.sel_issue.suggestion_pk,
                my_issue_pks: mine,
                other_issue_pks: others,
                similarity: false
            }).then(function (res) { // get issue list again 
                console.log(res)
                if(res.result){
                    const new_others = self.sel_issue.others
                    new_others.splice(new_others.indexOf(annot), 1)
                    self.unreviewed_issues=res.data.suggestions.filter(v => v.others.length>0)
                }
            });
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
            const box_id_list = JSON.parse(box_id)

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
                var texts = []
                var boxes = []

                boxes = resbox.filter(v => box_id_list.includes(v.box_id))
                texts = boxes.map(v => v.text)
                if (annot) {
                    annot.boxes_text = texts
                }

                //console.log(resbox)
                //console.log(texts)
                //console.log(boxes)

                return boxes
            })
        },

        async waitForJson(no, box_id, pk) {
            const response = await this.imageNo2Json(no, box_id, false)
            //console.log(response)
            if (this.annot_boxes[pk] === undefined) {
                this.$set(this.annot_boxes, pk, response)
                //console.log(this.annot_boxes)
            }
            return response
        },


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
    },


    watch: {
        sel_issue: {
            deep: true,
            handler() {
                //console.log("WATCH", this.sel_issue)
            }
        },
        /*
        annot_boxes: {
            deep: true,
            handler(after, before) {
                console.log("change in annot_boxes", this.annot_boxes)
                console.log(after, before)
            }
        },*/
    },

    computed: {
        ...mapGetters(['getImageBoxes']),
        valid_actual() {
            return (this.valid & true); // true 대신 this.issues_with_suggestions 가 0일때 true 하라고 넣으면 될듯!
        }
    },

}
</script>

<style scoped>

</style>