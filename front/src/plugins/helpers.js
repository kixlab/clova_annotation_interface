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
    isWrongAccess(self) {
      if (self.$store.state.mturk_id === null) {
        self.$router.push('landing')
        alert("You should register your mturk ID to proceed to the task.\n")
      }
    }
};