<template>
  <v-container pa-0 class="center">
    <v-card max-width="600" class="mx-auto my-12">
      <v-card-title class="text-center justify-center py-6">
        Anmelden
      </v-card-title>

      <v-tabs v-model="tab" background-color="transparent" grow>
        <v-tab> Nur mit E-Mail </v-tab>
        <v-tab> Mit Passwort </v-tab>
      </v-tabs>

      <v-tabs-items v-model="tab">
        <v-tab-item>
          <v-card>
            <v-card-text class="mt-5">
              <v-container v-if="!emailSend">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      label="E-Mail"
                      :error-messages="emailError"
                      type="email"
                      v-model="data_email.email"
                      v-on:keyup="onEmailTypInEmailField"
                      required
                    >
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-spacer />
                <v-btn
                  color="primary"
                  @click="onEmailLoginClick">
                  Link versenden
                </v-btn>
              </v-container>
              <v-container v-else>
                <v-row>
                  <v-col cols="12">
                    {{ 'Die Mail wurde erfolgreich an' }}
                    {{ data_password.email }}
                    {{ 'versendet. Bitte guck in dein Postfach' }}
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <v-tab-item>
          <v-card>
            <v-card-text class="mt-5">
              <v-container v-if="!emailSend">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      label="E-Mail"
                      :error-messages="emailError"
                      type="email"
                      v-model="data_password.username"
                      required
                    >
                    </v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      label="Passwort"
                      type="password"
                      v-model="data_password.password"
                      v-on:keyup="onEmailTypInEmailField"
                      required
                    >
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-spacer />
                <v-btn
                  color="primary"
                  @click="onPasswordLoginClick">
                  Einloggen
                </v-btn>
              </v-container>
              <v-container v-else>
                <v-row>
                  <v-col cols="12">
                    {{ 'Die Mail wurde erfolgreich an' }}
                    {{ data_email.email }}
                    {{ 'versendet. Bitte guck in dein Postfach' }}
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
    <v-snackbar
      v-model="showSuccess"
      color="success"
      y="top"
      :timeout="timeout"
    >
      Du hast eine E-Mail bekommen.
    </v-snackbar>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
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
    showSuccess: false,
    emailSend: false,
    timeout: 3000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    data_email: {
      email: '',
    },
    data_password: {
      username: '',
      password: '',
    },
    tab: null,
    items: ['Appetizers', 'Entrees'],
  }),
  computed: {
    emailError() {
      return [];
    },
  },
  methods: {
    onEmailTypInEmailField() {
    },
    onEmailLoginClick() {
      const me = this; // eslint-disable-line
      axios
        .post(`${this.API_URL}auth/register/`, this.data_email)
        .then((response) => {
          this.emailSend = true;
          this.onSuccessfulEmailSent(response);
        })
        .catch((error) => {
          this.responseObj = error.response.data[0]; // eslint-disable-line
          this.showError = true;
        });
    },
    onPasswordLoginClick() {
      const me = this; // eslint-disable-line
      axios
        .post(`${this.API_URL}auth/token/`, this.data_password)
        .then((response) => {
          this.$store.commit('setTokens', response.data.access, response.data.refresh);
          this.onSuccessfulLogin();
        })
        .catch((error) => {
          debugger;
          this.responseObj = error.response.data.detail; // eslint-disable-line
          this.showError = true;
        });
    },
    onSuccessfulEmailSent() {
      this.showSuccess = true;
    },
    onSuccessfulLogin() {
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
