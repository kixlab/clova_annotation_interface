import axios from 'axios'

export default {
    server_get(self, url, fn) {
      //console.log(self)
        axios.get(self.$store.state.server_url + url, {
          params: {
            mturk_id: self.$store.state.mturk_id
          }
        }).then(function (res) {
          fn.apply(this, [self, res])
        }).catch(function(err) {
          alert("Server is not responding\n" + err);
        });
    },
    server_post(self, url, fn) {
        axios.post(self.$store.state.server_url + url, {
          mturk_id: self.$store.state.mturk_id
        }).then(function (res) {
          fn.apply(this, [self, res])
        }).catch(function(err) {
          alert("Server is not responding\n" + err);
        });
    },
    server_log(self, type, box_ids, label='') {
      console.log(self, type, box_ids, label);
      /* axios.post(self.$store.state.server_url + '/api/log/', {
        mturk_id: self.$store.state.mturk_id,
        type: type,
        image_id : self.$store.state.image_order,
        box_ids : box_ids,
        label: label
      }).catch(function(err) {
        alert("Server is not responding\n" + err);
      }); */
  },
    isWrongAccess(self) {
      if (self.$store.state.mturk_id === null) {
        self.$router.push('landing')
        alert("You should register your mturk ID to proceed to the task.\n")
      }
    }
};