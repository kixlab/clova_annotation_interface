<template>
    <v-col cols="12">
        <v-card>
            <v-card-title>
                <h4>Overall interface</h4>
            </v-card-title>
            <v-text >
                <div style="min-height: 80vh; max-height: 90vh; overflow: scroll; padding: 0; margin-top: 6px;">
                    Still brainstorming layout
                </div>
            </v-text>
        </v-card>
    </v-col>
</template>

<script>
import axios from "axios";
//import {mapActions, mapGetters} from 'vuex';

export default {
    name: "OverallLabel",
    components: {

    },
    data() {
        return {
            worker: 'A8F6JFG0WSELT', // 지금 살펴보고자 하는 worker --> 나중에 worker정보 보여주는 view의 state로 가져가도 될듯!
            worker_list: [],
            worker_detail: {"username": null, "annotations":[], "start_time": null, "end_time":null},
            every_annotations: []
        };
    },

    mounted() {
        const self = this;

        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-workers',{
        params:{
            doctype: self.$route.params.docType
        }
        }).then(function(res){
            self.worker_list = res.data;
        })},500);

        setTimeout( function(){
        axios.get(self.$store.state.server_url+'/api/get-annotations-by-worker',{
        params:{
            mturk_id: self.worker
        }
        }).then(function(res){
            console.log(res.data);
        })},500);
    },

    methods: {

    },

    computed: {

    },

    watch: {

    },

}
</script>

<style scoped>

</style>