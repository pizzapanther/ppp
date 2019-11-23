var app = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {poll: PollComponent},
  data() {
    return {
      started: false,
      poll_data: JSON.parse(document.getElementById('poll-data').textContent)
    };
  },
  created() {
    Pusher.logToConsole = true;
    this.pusher = new Pusher('4650332133f87c946611', {
      cluster: 'us3',
      forceTLS: true
    });

    this.channel = this.pusher.subscribe(PRES.slug);
    this.channel.bind('stats', (data) => {
      this.stats(data)
    });
  },
  methods: {
    stats(data) {
      console.log(data);
    },
    start_poll() {
      fetch('./start', {method: 'POST'})
        .then((response) => {
          if (response.status == 200) {
            this.started = true;
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
