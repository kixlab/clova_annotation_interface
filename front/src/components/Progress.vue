<template>
<div class='center'>
  <div style="width: 100%; overflow-x: auto; overflow-y: hidden; position: relative; white-space: nowrap;">
      <template v-for="(status, index) in stats"> 
        <template v-if="index===curr_index">
          <template v-if="status===true">
            <button class="curr done status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
          <template v-else>
            <button class="curr yet status" v-on:click="goTo(index);" :key='index'>
            #{{index+1}}
            </button>
          </template>
        </template>
        <template v-else>
          <template v-if="status===true">
            <button class="done status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
          <template v-else>
            <button class="yet status" v-on:click="goTo(index);" :key='index' >
            #{{index+1}}
            </button>
          </template>
        </template>
      </template>

  </div>
<!--  <div>
  {{stats}}
 </div>
 --></div>
</template>


<script>
import { mapActions, mapGetters} from 'vuex'

export default {
  name: "Progress",
  data() {
    return {
      curr_index: this.$store.getters.get_image_order
    };
  },
  mounted() {
    this.$store.subscribeAction({after: (action) => {
        if (action.type ==='setCurrImage') {
            this.curr_index = this.$store.getters.get_curr_image
        }
    }})

  },
  computed: {
    stats() {
          return this.$store.getters.getStatus;
        }
  },
  watch: {

    curr_image_no:{
      deep: true, 
      handler(){
        this.curr_index = this.$store.getters.get_curr_image
      }
      },
    stats() {
          return this.$store.getters.getStatus;
        }
  }, 
  methods:{
      ...mapActions(['setCurrImage', 'setCurrOrder']),
      ...mapGetters(['getStatus']),
      goTo: function(index){
        this.$store.commit('set_image_order', index);
        this.setCurrOrder(index)
        this.setCurrImage(index)
      },
  }
};
</script>

<style scoped>
.center{
  margin:auto;
  width: 90% !important;
}
table{
  width: 100% !important;
  overflow-x: scroll;
}
.status{
  margin: 1px;
  border: 1px solid grey;
  border-radius: 2% !important;
  width: 4%!important;
  cursor:pointer !important;
  
}
.yet{
  background-color: rgba(180, 180, 180, 0.548);
}
.done{
  background-color: rgba(79, 192, 79, 0.548) !important;
}

.curr{
  border: 2px solid red !important;
}
</style>
