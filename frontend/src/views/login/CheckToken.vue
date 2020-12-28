<template>
  <v-container class="max-width-class" pa-0>
    <div class="text-center" v-if="!fail">
      <v-progress-circular
        :size="120"
        :width="10"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </div>
    <v-card v-else>
      <v-toolbar dark color="primary">
        <v-toolbar-title>
          {{ 'Check token' }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-card-text class="mt-5">
        <p>{{ this.$route.query.test }}</p>
        <p>
          Wir überprüfen deinen token und leiten dich dann in den internen
          bereich weiter
        </p>
        <v-btn @click="onButtonClick"> Klicke hier </v-btn>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
      {{ responseObj }}
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data: () => ({
    showError: false,
    emailSend: false,
    timeout: 3000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    fail: false,
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
      const me = this;
      axios
        .post(`${this.API_URL}auth/token/`, {
          username: this.$route.query.username,
          password: this.$route.query.password,
        })
        .then((response) => {
          this.$store.commit(
            'setTokens',
            response.data.access,
            response.data.refresh,
          );
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
  mounted() {
    const me = this;
    this.onButtonClick();
    setTimeout(() => {
      me.fail = true;
    }, 2000);
  },
};
</script>
