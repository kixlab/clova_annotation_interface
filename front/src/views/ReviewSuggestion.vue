<template>
  <v-app class="annotation">
    <v-app-bar
      app
      color="indigo lighten-1"
      dark
      dense
      fixed
    >
      <v-toolbar-title>Image Annotation (ID: {{this.$store.state.mturk_id}})</v-toolbar-title>
      <v-spacer/>
      <review-instruction-button/>

    <v-tooltip bottom :disabled="valid">
            <template v-slot:activator="{ on, attrs }">
            <div v-on="on">
            <v-btn
                class="ma-2"
                :disabled="!valid"
                color="error"
                @click="onSubmit"
                v-bind="attrs"
                v-on="on"
            >
                Next
            </v-btn>
            </div>
            </template>
            Mark the similarity for every suggestions you have made. 
        </v-tooltip>
      </v-app-bar>

     <v-main>
      <v-container v-if="enough_suggestions" fluid fill-height>
        <v-row align-content='center'>
            <v-col>
                <h3>In this page, we ask you to choose annotations <u>that represent similar suggestions</u>.</h3>
                <h3> After finishing marking similar suggestions, click the button on the top right to proceed to post-survey.</h3>
            </v-col>
        </v-row>
        <v-row  align-content='center' style="border: 0px solid red; height: 100%; overflow-y: auto">
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
                                <v-btn depressed :outlined="v.suggestion_pk !== sel_issue.suggestion_pk" color="warning" small style="margin: 5px" @click="clickCloseto(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                ({{v.n_issues}})
                            </div>
                            <h4 style="text-align: left; margin-top: 10px">N/A Suggestions</h4>
                            <div v-for="(v, idx) in unreviewed_issues.filter(v => v.suggestion_subcat === 'n/a')" :key="'n/a-' + idx" style="overflow-y: scroll">
                                <v-btn depressed :outlined="v.suggestion_pk !== sel_issue.suggestion_pk" color="error" small style="margin: 5px" @click="clickNa(v)"> 
                                    {{v.suggestion_cat}}-{{v.suggestion_subcat}} ({{v.suggestion_text}})
                                </v-btn>
                                ({{v.n_issues}})
                            </div>
                        </v-col>
                        <v-col cols="3" style="border: 1px solid black; ">
                            <h3>Your annotations for with this suggestion.</h3>
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
                            <h3>Check whether each suggestion is similar to yours. ({{sel_issue.others.length}} to review)</h3>
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
            </v-col>
        </v-row>
    </v-container>
    <v-container v-else fluid fill-height>
        <v-row align-content='center'>
            <v-col>
                <h3>There is no enough others' suggestions to compare with yours. You can skip this 'review' process and proceed to post-survey. Click 'NEXT' button on the top right!</h3>
            </v-col>
        </v-row>
    </v-container>
    </v-main>
  </v-app>

    
</template>

<script>
import axios from "axios";
import BoundingBox from '@/components/BoundingBox.vue'
import ReviewInstructionButton from "@/components/ReviewInstructionButton.vue"
import {mapGetters} from 'vuex';

export default {
    name: 'ReviewSuggestion',
    components: {
        BoundingBox,
        ReviewInstructionButton,
    },
    data () {
        return {
            issue_list: [],
            sel_issue: {
                mine:[],
                others: []
            },

            enough_suggestions: true,

            sel_sim_issues: [],

            unreviewed_issues: [], // 내가 한 suggestion 단위로 없어짐
            issues_with_suggestions:[], // 처음에 mount 함




            // Related to the survey
            valid: false,
        

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
            self.valid=(self.unreviewed_issues.length==0);
            self.enough_suggestions=res.data.status;
            if(!self.enough_suggestions){
                self.valid=true;
            }
        })
    },

    methods: {
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
                if(res.data.result){
                    const new_others = self.sel_issue.others
                    new_others.splice(new_others.indexOf(annot), 1)

                    self.unreviewed_issues=self.issues_with_suggestions.filter(v => v.others.length>0)
                    self.valid=(self.unreviewed_issues.length==0);
                }else{
                    window.alert('Error!')
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
                other_issue_pk: others,
                similarity: false
            }).then(function (res) { // get issue list again 
                console.log(res)
                if(res.data.result){
                    const new_others = self.sel_issue.others
                    new_others.splice(new_others.indexOf(annot), 1)

                    self.unreviewed_issues=self.issues_with_suggestions.filter(v => v.others.length>0);
                    self.valid=(self.unreviewed_issues.length==0);
                }else{
                    window.alert('Error!')
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
        onSubmit: function() {
            const self=this;
            axios.post(self.$store.state.server_url + '/api/review-done/', {
                mturk_id: self.$store.state.mturk_id,
            }).then( function(){
                self.$router.push('../../postsurvey/');
            });


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