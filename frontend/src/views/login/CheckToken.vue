<template>
  <v-container class="max-width-class" pa-0>
    <v-card>
      <v-toolbar dark color="primary">
        <v-toolbar-title>
          {{ 'Check token' }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-card-text class="mt-5">
        <p>{{ this.$route.query.test }}</p>
        <p>Wir überprüfen deinen token und leiten dich dann in den internen bereich weiter</p>
        <v-btn
          @click="onButtonClick"
        >
          Klicke hier
        </v-btn>
      </v-card-text>
    </v-card>
    <v-snackbar
      v-model="showError"
      color="error"
      y='top'
      :timeout="timeout"
    >
      {{ responseObj }}
    </v-snackbar>
</v-container>
</template>

<script>
import axios from 'axios';
import { email, required } from 'vuelidate/lib/validators';

export default {
  name: 'Login',
  data: () => ({
    showError: false,
    emailSend: false,
    timeout: 3000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    data: {
      email: '',
    },
  }),
  computed: {
    emailError() {
      return [];
    },
  },
  methods: {
    onButtonClick() {
      const me = this; // eslint-disable-line
      axios.post(`${this.API_URL}api/token/`, {
        username: this.$route.query.username,
        password: this.$route.query.password,
      })
        .then((response) => {
          this.$store.commit('setTokens', response.data.access, response.data.refresh);
          debugger;
          this.emailSend = true;
          this.onSuccessfulLogin();
        })
        .catch((error) => {
          this.responseObj = error.response.data.detail;
          this.showError = true;
        });
    },
    onSuccessfulLogin() {
      this.$store.commit('setCurrentUser', this.data.username);
      this.$router.push({ name: 'eventOverview' });
    },
  },
  validators: {
    email: {
      email,
      required,
    },
  },
};
</script>

<style scoped>

</style>
