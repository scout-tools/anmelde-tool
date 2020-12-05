<template>
  <v-container class="max-width-class" pa-0>
    <v-card>
      <v-toolbar dark color="primary">
        <v-toolbar-title>
          {{ 'Header' }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-card-text class="mt-5">
        <div v-if="!emailSend">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                label="E-Mail"
                :error-messages="emailError"
                type="email"
                v-model="data.email"
                v-on:keyup="onEmailTypInEmailField"
                required>
              </v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <v-container>
          <v-spacer/>
          <v-btn
            large
            @click="onLoginClick">
            Einloggen
          </v-btn>
        </v-container>
        </div>
        <div v-else>
          <v-container>
            <v-row>
              <v-col cols="12">
                {{ 'Die Mail wurde erfolgreich an X@b.de versendet. Bitte guck in dein Postfach' }}
              </v-col>
            </v-row>
          </v-container>
        </div>
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
    onEmailTypInEmailField(event) { // eslint-disable-line
      if (event.code === 'Enter') {
        this.onLoginClick();
      }
    },
    onLoginClick() {
      const me = this; // eslint-disable-line
      axios.post(`${this.API_URL}api/token/`, this.data)
        .then((response) => {
          this.$store.commit('setTokens', response.data.access, response.data.refresh);
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
