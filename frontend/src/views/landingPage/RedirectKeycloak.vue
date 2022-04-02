<template>
  <v-container class="top-margin" v-if="!isLoading">
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
    <v-row>
      <Circual v-if="isLoading"/>
    </v-row>
  </v-container>

</template>

<script>
import authMixin from '@/mixins/authMixin';
import Circual from '@/components/loading/Circual.vue';

export default {
  mixins: [authMixin],
  components: {
    Circual,
  },
  data() {
    return {
      interval: {},
      value: 0,
      isLoading: true,
    };
  },
  beforeDestroy() {
  },
  created() {
    this.isLoading = true;
  },
  mounted() {
    this.isLoading = true;
    setInterval(() => { // eslint-disable-line
      if (this.isAuth) {
        this.$router.push({ name: 'eventOverview' });
      } else {
        this.isLoading = false;
      }
      this.handleLogic();
    }, 100);
  },
  methods: {
    login() {
      this.$keycloak.login();
      this.$store.commit('setAccountIncomplete', true);
    },
    handleLogic() {
      setInterval(() => { // eslint-disable-line
        if (this.isAuth) {
          this.$router.push({ name: 'eventOverview' });
        }
        if (this.value === 75) {
          this.login();
        }
        this.value += 25;
      }, 700);
    },
  },
};
</script>

<style scoped>
.v-progress-circular {
  margin: 1rem;
}
</style>
