
const state = {
    annot_status: new Array(20).fill(false)
}

const getters = {
    getStatus: (state) => {
        return state.annot_status
      },
    getIfAllImagesAnnotated: function (state) {
    return state.annot_status.every(status => status === true)
    },
}

const actions = {
    setStatus({commit}, status){
        //console.log('setStatus called with', status)
        commit('update_status', status)
      },
    setAStatus({commit}, payload){
        var new_status = this.state.workers.annot_status
        new_status[payload.idx] = payload.val
        commit('update_a_status', new_status)      
    },  
}

const mutations = {
    update_status(state, status){
        state.annot_status=status
    },
    update_a_status(state, new_status){
        state.annot_status = new Array(20).fill(false)
        state.annot_status = new_status
    },
  
}

export default {
    state,
    getters,
    actions,
    mutations
}