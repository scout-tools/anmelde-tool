<template>
  <v-container pa-0 class="center">
    <v-card max-width="500" class="mx-auto my-12">
      <v-card-title class="text-center justify-center py-6">
        Anmelden
      </v-card-title>

      <v-tabs v-model="tab" background-color="transparent" grow>
        <v-tab> Mit E-Mail </v-tab>
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
                      :disabled="isEmailFieldIsLoading"
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
                <v-btn color="primary" @click="onEmailLoginClick">
                  Link versenden
                </v-btn>
              </v-container>
              <v-container v-else>
                <v-row>
                  <v-col cols="12">
                    {{ 'Du hast eine E-Mail auf deine Adresse' }}
                    {{ data_email.email }}
                    {{ 'erhalten. Bitte guck in dein Postfach und benutze den Link zum einloggen' }}
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
                <v-btn color="primary" @click="onPasswordLoginClick">
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
    isEmailFieldIsLoading: false,
    data_email: {
      email: '',
    },
    data_password: {
      username: '',
      password: '',
    },
    tab: null,
  }),
  computed: {
    emailError() {
      return [];
    },
  },
  methods: {
    onEmailTypInEmailField() {},

    callRegisterPost() {
      return axios.post(`${this.API_URL}auth/register/`, this.data_email);
    },

    callTokenPost() {
      return axios.post(`${this.API_URL}auth/token/`, this.data_password);
    },

    callLoginPost() {
      return axios.post(`${this.API_URL}auth/login/`, this.data_email);
    },

    onEmailLoginClick() {
      this.handleLoginRequest();
    },

    onPasswordLoginClick() {
      this.isEmailFieldIsLoading = true;
      this.handlePasswordLoginRequest();
    },

    async handleEmailLoginRequest() {
      try {
        const response = await this.callRegisterPost();
        this.emailSend = true;
        this.onSuccessfulEmailSent(response);
        this.isEmailFieldIsLoading = false;
      } catch (error) {
        this.responseObj = error.response.data[0]; // eslint-disable-line
        this.showError = true;
        this.isEmailFieldIsLoading = false;
      }
    },

    async handlePasswordLoginRequest() {
      try {
        const response = await this.callTokenPost();
        this.$store.commit(
          'setTokens',
          response.data.access,
          response.data.refresh,
        );
        this.onSuccessfulLogin();
      } catch (error) {
        this.responseObj = error.response.data.detail; // eslint-disable-line
        this.showError = true;
      }
    },

    async handleLoginRequest() {
      try {
        const response = await this.callLoginPost();
        if (response.data.message === 'Login email sent') {
          this.isEmailFieldIsLoading = false;
          this.emailSend = true;
        }
      } catch (error) {
        if (error.response.status === 500) {
          this.handleEmailLoginRequest();
        } else {
          this.showError = true;
        }
        this.isEmailFieldIsLoading = false;
      }
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
