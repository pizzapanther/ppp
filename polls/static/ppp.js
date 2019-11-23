var app = new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  created() {
    Pusher.logToConsole = true;
    this.pusher = new Pusher('4650332133f87c946611', {
      cluster: 'us3',
      forceTLS: true
    });

    this.channel = this.pusher.subscribe(PRES.slug);
    this.channel.bind('go-live', (data) => {
      this.go_live(data)
    });
  },
  methods: {
    go_live(data) {
      console.log(data);
    }
  }
});
