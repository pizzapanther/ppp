Vue.use(VueApexCharts);
Vue.component('apexchart', VueApexCharts);

var app = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {poll: PollComponent},
  data() {
    return {
      started: false,
      poll_data: JSON.parse(document.getElementById('poll-data').textContent),
      time: 0
    };
  },
  created() {
    Pusher.logToConsole = true;
    this.pusher = new Pusher(PRES.key, {
      cluster: 'us3',
      forceTLS: true
    });

    this.channel = this.pusher.subscribe(PRES.slug);
    this.channel.bind('stats', (data) => {
      if (JSON.stringify(this.poll_data.votes) != JSON.stringify(data.votes)) {
        this.poll_data = data;
      }
    });
  },
  methods: {
    stats(data) {
      console.log(data);
    },
    update_time() {
      this.time += 1;
      if (this.started) {
        setTimeout(() => {
          this.update_time();
        }, 1000);
      }
    },
    start_poll() {
      fetch('./start', {method: 'POST'})
        .then((response) => {
          if (response.status == 200) {
            this.started = true;
            this.time = 0;
            setTimeout(() => {
              this.update_time();
            }, 1000);
          } else {
            alert(response.status);
          }
        })
        .catch((e) => {
          alert(e);
        });
    },
    end_poll() {
      fetch('./end', {method: 'POST'})
        .then((response) => {
          if (response.status == 200) {
            this.started = false;
          } else {
            alert(response.status);
          }
        })
        .catch((e) => {
          alert(e);
        });
    }
  }
});
