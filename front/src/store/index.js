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
    server_url: 'http://52.78.121.66:8000',

    assigned_images: [],
    start_image_no: 0,
    image_order: 0,
    curr_image_no: 0,
  },
  mutations: {
    set_image_order (state, cnt) {
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
    set_server_url(state, server_url) {
      state.server_url = server_url
    },
    
  },
  getters: {
    image_url: (state) => {
      var docType= router.currentRoute.params.docType
     // var image_order=state.image_order+state.start_image_no;
      
      var three_digit_id = ("00" + state.curr_image_no).slice(-3);
      //console.log("server_url ** ", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png')
      return 'http://52.78.121.66:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
      
    },
    json_url: (state) => {
      var docType= router.currentRoute.params.docType
      //var image_order=state.image_order+state.start_image_no;

      var three_digit_id = ("00" + state.curr_image_no).slice(-3);
      //console.log("json_url **", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json')
      return 'http://52.78.121.66:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
    },
    prac_image_url: () => {
      var docType= router.currentRoute.params.docType
     // var image_order=state.image_order+state.start_image_no;
      
      var three_digit_id = '813';
 //     console.log("server_url ** ", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png')
      return 'http://52.78.121.66:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.png'
      
    },
    prac_json_url: (state) => {
      var docType= router.currentRoute.params.docType
      //var image_order=state.image_order+state.start_image_no;

      var three_digit_id = '813';
      console.log("json_url **", state.server_url + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json')
      return 'http://52.78.121.66:8000' + '/media/'+docType+'/'+docType+'_00' + three_digit_id + '.json'
    },
    get_image_order: state =>{
      return state.image_order
    },
    get_curr_image: (state) => {
      return state.curr_image_no
    },
    get_assigned_images: (state) => {
      return state.assigned_images
    },
    get_server_url: (state) => {
      return state.server_url
    },
  },
  actions:{
    setCurrOrder({commit}, neworder){
      commit('set_image_order', neworder)
    },
    setCurrImage({commit}, newidx) {
      commit('set_curr_image', newidx)
    },
    setAssignedImages({ commit }, images) {
      commit('set_assigned_images', images)
    },  
    setServerURL({commit}, newURL) {
      commit('set_server_url', newURL)
    } ,


    
  },
  modules: {
    images,
    workers,
  }
})
