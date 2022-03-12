<template>
  <v-dialog
    v-model="dialog"
    width="80%"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        outlined
        v-bind="attrs"
        v-on="on"
        @click="openInstruction"
      >
        Instruction
      </v-btn>
    </template>

    <v-card tile class="instruction">
      <v-card-title>
       <b># Instruction</b>
      </v-card-title>
      <v-card-subtitle> 
       <b>Please refer to the below instructions along the way.</b>
      </v-card-subtitle>
      <div v-for="num in [1, 2, 3]" :key="num">
        <v-img :src="require('@/assets/instruction-review'+num+'.png')" style="width: 75%; margin: 8px auto; box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);"/>
      </div>

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
export default {
    name: "ReviewInstructionButton",
    data() {
        return {
          dialog: false,
        };
    },

    methods: {
      openInstruction: function () {
        const self=this;
        self.dialog = true;
      }
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
</style>