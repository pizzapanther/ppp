Vue.use(VueApexCharts);
Vue.component('apexchart', VueApexCharts);

var app = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  components: {poll: PollComponent},
  data() {
    var poll_data = null;
    var ele = document.getElementById('current');
    if (ele) {
      poll_data = JSON.parse(ele.textContent);
    }

    return {
      poll_data: poll_data
    };
  },
  created() {
    Pusher.logToConsole = true;
    this.pusher = new Pusher(PRES.key, {
      cluster: 'us3',
      forceTLS: true
    });

    this.channel = this.pusher.subscribe(PRES.slug);
    this.channel.bind('go-live', (data) => {
      this.poll_data = data;
    });
    this.channel.bind('end-poll', (data) => {
      this.poll_data = null;
    });
    this.channel.bind('stats', (data) => {
      if (!this.poll_data) {
        this.poll_data = data;
      } else if (JSON.stringify(this.poll_data.votes) != JSON.stringify(data.votes)) {
        this.poll_data = data;
      }
    });
  },
  methods: {
  }
});
