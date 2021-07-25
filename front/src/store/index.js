import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import router from '../router'
import images from './modules/images'
import workers from './modules/workers'

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  state: {
    mturk_id: null,
    doctype: null,
    server_url: 'http://13.125.191.49:8000',

    assigned_images: [],
    start_image_no: 0,
    image_order: 0,
    curr_image_no: 0,
  },
  mutations: {
    set_image_order (state, cnt) {
      console.log('image order set to ', cnt)
      state.image_order = cnt;
    },
    update_image_count (state) {
      state.image_order++;
    },
    set_mturk_id (state, id){
      state.mturk_id = id
    },
    set_assigned_images(state, assigned_images){
      state.assigned_images=assigned_images
    },
    set_start_image_no(state, img_no){
      state.start_image_no=img_no
    },
    set_step (state, step){
      state.step = step
    },
    set_curr_image(state, newidx) {
      var new_image=state.assigned_images[newidx]
      state.curr_image_no = new_image
    },
    
  },
  getters: {
    image_url: state => {
      var docType= router.currentRoute.params.docType
     // var image_order=state.image_order+state.start_image_no;
      
      var three_digit_id = ("00" + state.curr_image_no).slice(-3);
//      console.log(state.start_image_no);
      console.log("server_url ** ", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png')
      return state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
      
    },
    json_url: state => {
      var docType= router.currentRoute.params.docType
      //var image_order=state.image_order+state.start_image_no;

      var three_digit_id = ("00" + state.curr_image_no).slice(-3);
      console.log("json_url **", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json')
      return state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
    },
    get_image_order: state =>{
      return state.image_order
    },
    get_curr_image: (state) => {
      return state.curr_image_no
    },
    get_assigned_images: (state) => {
      return state.assigned_images
    }
  },
  actions:{
    setCurrOrder({commit}, neworder){
      commit('set_image_order', neworder)
    },
    setCurrImage({commit}, newidx) {
      console.log('setCurrImage called')
      commit('set_curr_image', newidx)
    },
    setAssignedImages({ commit }, images) {
      commit('set_assigned_images', images)
  },  

    
  },
  modules: {
    images,
    workers,
  }
})
