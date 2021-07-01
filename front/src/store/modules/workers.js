
const state = {
    assignedImages: [],
    annotatedImages: [],
    annnot_status: new Array(21).fill(false)
}

const getters = {
    getAssignedImages: (state) => state.assignedImages,
    getAnnotatedImages: (state) => state.annotatedImages,
    getStatus: (state) => {
        return state.annot_status
      },
}

const actions = {
    initalizeImages({ commit }) {
        const fromServer = ['00001', '00002', '00003', '00004']
        const assigned = fromServer.map(function(i) {
            return {
                image_id: i,
                annotated: false,
                start_time: Date(),
                end_time: '',
            }
        })
        console.log("$$ INITIALIZE crowd $$", assigned)
        commit('setAssignedImages', assigned)
    },

    updateAssignedImages({ commit }, images) {
        const annotated = images.filter(v => v.annotated === true)

        commit('setAssignedImages', images)
        commit('setAnnotatedImages', annotated)
    },  
    setStatus({commit}, status){
        //console.log('setStatus called with', status)
        commit('update_status', status)
      },
    setAStatus({commit}, payload){
        var new_status = this.state.annot_status
        console.log('before payload', new_status)
        new_status[payload.idx] = payload.val
        console.log('after payload', new_status)
        commit('update_a_status', new_status)      
    },
}

const mutations = {
    setAssignedImages: (state, assignedImages) => {
        state.assignedImages = assignedImages
    },
    setAnnotatedImages: (state, annotatedImages) => {
        state.annotatedImages = annotatedImages
    },
    update_status(state, status){
        console.log("old",state.annot_status)
        console.log("new",status)
        state.annot_status=status
    },
    update_a_status(state, new_status){
        console.log('before', state.annot_status)
        state.annot_status = new Array(21).fill(false)
        console.log('before', state.annot_status)
        state.annot_status = new_status
        console.log('after', state.annot_status)
    },
  
}

export default {
    state,
    getters,
    actions,
    mutations
}