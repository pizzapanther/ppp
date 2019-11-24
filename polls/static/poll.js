var PollComponent = {
  props: ['data', 'admin'],
  template: `
<div class="poll">
  <h2>{{ data.question }}</h2>
  <div class="choices" v-if="!admin">
    <v-btn v-for="(choice, index) in data.choices"
      :key="index"
      color="accent"
      @click="do_vote(index)"
      :disabled="voted == data.id"
    >
      {{ choice }}
    </v-btn>
  </div>
  <div class="donut">
    <apexchart type=donut width=380 :options="opts" :series="series" />
  </div>
</div>`,
  data() {
    return {
      voted: false
    }
  },
  mounted() {
    this.voted = false;
  },
  computed: {
    opts() {
      var labels = [];
      this.data.choices.forEach((c) => {
        labels.push(c);
      });
      return {
        labels: labels
      };
    },
    series(){
      return this.data.votes;
    }
  },
  methods: {
    do_vote(index) {
      var formData = new FormData();
      formData.append('vote', index);
      formData.append('poll', this.data.id);

      fetch('./vote', {method: 'POST', body: formData})
        .then((response)=> {
          if (response.status == 200) {
            this.voted = this.data.id;
          } else {
            alert(response.status);
          }
        })
        .catch((e) => {
          alert(e);
        })
    }
  }
};
