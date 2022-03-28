<template>
  <v-container class="top-margin">
    <v-row align="center" justify="center" class="ma-10">
      <p>
        Du wirst in 5 Sekunden zum DPV-Login weitergeleitet. Nachdem du dich
        authorisiert hast gelangst du zurück in das Anmelde-Tool
      </p>
    </v-row>
    <v-row align="center" justify="center" class="ma-10">
      <v-progress-circular
        :rotate="360"
        :size="100"
        :width="15"
        :value="value"
        color="teal"
      >
        {{ value }} %
      </v-progress-circular>
      <p>bis zur Weiterleitung</p>
    </v-row>
    <v-row align="center" justify="center" class="ma-10">
      <v-btn color="primary">Zurück zum Anmelde-Tool</v-btn>
    </v-row>
  </v-container>
</template>

<script>
import authMixin from '@/mixins/authMixin';

export default {
  mixins: [authMixin],
  data() {
    return {
      interval: {},
      value: 0,
    };
  },
  beforeDestroy() {
    clearInterval(this.interval);
  },
  mounted() {
    this.interval = setInterval(() => { // eslint-disable-line
      if (this.isAuth) {
        this.$router.push({ name: 'eventOverview' });
      }
      if (this.value === 100) {
        this.login();
        return (this.value = 0); // eslint-disable-line
      }
      this.value += 25;
    }, 700);
  },
  methods: {
    login() {
      this.$keycloak.login();
      this.$store.commit('setAccountIncomplete', true);
    },
  },
};
</script>

<style scoped>
.v-progress-circular {
  margin: 1rem;
}
</style>
