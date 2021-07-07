<template>
  <v-dialog
    v-model="dialog"
    width="70%"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        outlined
        v-bind="attrs"
        v-on="on"
        @click="openOverview"
      >
        Overview
      </v-btn>
    </template>

    <v-card tile class="instruction">
      <v-card-title>
       <b># Overview</b>
      </v-card-title>
      <v-card-subtitle> 
       <b>Click a document image that you want to annotate or review. </b>
      </v-card-subtitle>
      <ul>
          <v-list-item v-for="(row, index) in options" :key='index'>
              <v-card class="pa-2 imgno" style="align-self:baseline; width:80%" height='inherit' v-for="(number, subindex) in row" :key='subindex' v-on:click="goTo(number);" @click="dialog = false">
                  #{{number+1}}
                  <img style='width:100%' v-bind:src="getThumbnail(number)">
              </v-card>
              </v-list-item>
      </ul>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="primary"
          text
          @click="dialog = false"
        >
          Exit
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {mapActions} from 'vuex';

export default {
    name: "OverviewButton",
    data() {
        return {
          dialog: false,
          options: [Array.from(Array(4).keys()), Array.from(Array(4).keys()).map(function(item){return item+4;}), Array.from(Array(4).keys()).map(function(item){return item+8;}), Array.from(Array(4).keys()).map(function(item){return item+12;}), Array.from(Array(4).keys()).map(function(item){return item+16;})],
          docType: this.$route.params.docType
        };
    },

    methods: {
      ...mapActions(['setImageBoxes', 'updateAnnotatedBoxes',]),

      openOverview: function () {
        const self=this;
        self.dialog = true;
        self.$helpers.server_log(self, 'RI', [])
      },
      goTo: function(imgNo){
        this.$store.commit('set_image_count', imgNo);
        this.image_box = this.$store.getters.getImageBoxes;

      },
      getThumbnail: function (imgNo){
        var docType= this.$route.params.docType;
        var two_digit_id = ("0" + imgNo).slice(-2);
        return 'http://13.125.191.49:8000'+ '/media/'+docType+'/'+docType+'_000' + two_digit_id + '.png'
      },      
    },
    mounted() {
      // this.dialog = true;
    },
}
</script>

<style scoped>
.instruction {
  text-align: left;
  padding-left: 20px;
}
.red-text {
  color:red;
  font-weight: bold;
}
.blue-text {
  color:blue;
  font-weight: bold;
}
.gray-text {
  color:gray;
  font-weight: bold;
}
.bold-text {
  font-weight: bold;
}
.imgno{
  width: 5% !important;
}
</style>