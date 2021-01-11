<template>
  <div
    class="bg"
    :style="{
      'background-image':
        'url(' + require('@/assets/2018-05-Führungstippel-63_klein.jpg') + ')',
    }"
  >
    <v-container fill-height fluid>
      <v-row align="center" justify="center">
        <v-col>
          <v-card
            max-width="500"
            min-width="350px"
            class="mx-auto my-12"
            color="rgb(255, 255, 255, 0.8)"
          >
            <v-card-title class="text-center justify-center py-6">
              Ich möchte mich einloggen
            </v-card-title>

            <v-card-text class="mt-5">
              <v-container v-if="!emailSend && !isEmailFieldIsLoading">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      :disabled="isEmailFieldIsLoading"
                      label="Deine E-Mail Adresse"
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
                  Absenden
                </v-btn>
              </v-container>

              <v-container class="text-center" v-if="isEmailFieldIsLoading">
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </v-container>

              <v-container v-if="emailSend">
                <v-row>
                  <v-col cols="12">
                    {{ 'Du hast eine E-Mail auf deine Adresse' }}
                    {{ data_email.email }}
                    {{
                      'erhalten. Bitte guck in dein Postfach und benutze den Link zum einloggen'
                    }}
                  </v-col>
                </v-row>
                  <v-row>
                  <v-col>
                    <v-btn color="primary" @click="emailSend = false">
                      <v-icon>
                        mdi-refresh
                      </v-icon>
                      Mit einer anderen E-Mail einloggen
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
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
    imageLink: {
      sub_main:
        'https://wiki.hratuga.de/files/public-docs/2018-05-Fu%CC%88hrungstippel-63-klein.jpg',
      main:
        'https://wiki.hratuga.de/files/public-docs/2018-05-Fu%CC%88hrungstippel-63_klein.jpg',
      logo: 'https://wiki.hratuga.de/files/public-docs/logo_bdp_dpv.png',
      social_cover:
        'https://firebasestorage.googleapis.com/v0/b/endorfinevue.appspot.com/o/assets%2Fo-NIGHTCLUB-facebook.jpg?alt=media&token=cefc5c4c-9714-41da-9c22-f63caf5e89a4',
    },
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

    handleEmailLoginRequest() {},

    handleLoginRequest() {
      this.isEmailFieldIsLoading = true;

      this.callLoginPost()
        .then(() => {
          this.emailSend = true;
        })
        .catch(() => {
          debugger;

          this.showError = true;
        })
        .then(() => {
          this.isEmailFieldIsLoading = false;
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

<style>
.bg {
  /* The image used */

  /* Full height */
  height: 100%;

  /* Center and scale the image nicely */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}
</style>
