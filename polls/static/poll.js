var PollComponent = {
  props: ['data', 'admin'],
  template: `
<div class="poll">
  <h3 class="location" v-if="admin">
    <span>{{ location.hostname }}/{{ data.slug }}</span>
    <br>
    <span>Votes: {{ data.total }}</span>
  </h3>
  <h2>{{ data.question }}</h2>
  <div v-if="admin" class="admin-questions">
    <div v-for="(choice, index) in data.choices" :key="index">
      <strong>{{ index + 1 }}. {{ choice }}</strong>
    </div>
  </div>
  <div class="choices" v-else>
    <v-btn v-for="(choice, index) in data.choices"
      small
      :key="index"
      color="accent"
      @click="do_vote(index)"
      :disabled="voted == data.id"
    >
      {{ choice }}
    </v-btn>
  </div>
  <div class="donut">
    <apexchart type=donut width=300 :options="opts" :series="series" />
  </div>
  <div v-if="!admin">Votes: {{ data.total }}</div>
</div>`,
  data() {
    return {
      voted: false,
      location: location
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
        labels: labels,
        legend: {
          position: 'bottom'
        }
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
