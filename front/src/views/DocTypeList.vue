<template>
  <v-row justify="center" align-content="center" align="center" class="instr">
    <v-col cols="8">
      <v-list >
          <v-list-item-group 
            mendatory 
            active-class="border" 
            color="indigo"
          >
            <v-list-item v-for="(doctype, index) in doctypes" :key='index' @click="gotoDoc(doctype)">
              <b>{{doctype}}</b>
            </v-list-item>
          </v-list-item-group>

      </v-list>
    </v-col>
  </v-row>
</template>

<script>
import axios from "axios";

export default {
  name: 'DocTypeList',
  data: () => ({
    doctypes: []
  }),
  mounted(){
    const self = this;
      axios.get(self.$store.state.server_url + "/api/get-doctypes").then(function(res){
          self.doctypes=res.data.doctypes;
      })  
    }
      ,
  methods: {
    gotoDoc: function(doctype){
      const self = this;
      self.$router.push('../annotation/'+doctype);
    },
    beforeCreate() {
      this.$helpers.isWrongAccess(this)
    }
}
}
</script>
<style scoped>
.instr {
  height: 100%;
  text-align: left;
}
</style>