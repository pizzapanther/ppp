var PollComponent = {
  props: ['data'],
  template: `
<div>
  <h2>{{ data.question }}</h2>
  <ul>
    <li v-for="(choice, index) in data.choices">
      {{ choice }}
    </li>
  </ul>
</div>`
};
