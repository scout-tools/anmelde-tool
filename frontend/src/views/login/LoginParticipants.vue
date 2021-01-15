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
            color="rgb(255, 255, 255, 0.9)"
          >
            <v-card-title class="text-center justify-center py-6">
              Einloggen
            </v-card-title>
            <v-card-text class="mt-5">
              <v-subheader
                >Gebe hier deine E-Mail-Adresse an. Den Link zur Anmeldung und
                den Aktionen bekommst du dann per Mail. Für ein erneutes
                Einloggen benutze den Link aus der Mail oder gebe deine E-Mail
                einfach erneut an.</v-subheader
              >
              <v-container v-if="!emailSend && !isEmailFieldIsLoading">
                <v-row>
                  <v-col cols="12">
                    <v-text-field
                      v-model="email"
                      label="Deine E-Mail Adresse"
                      prepend-icon="mdi-email"
                      :error-messages="emailError"
                      v-on:keyup="onEmailTypeInEmailField"
                    >
                      <template slot="append">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-icon
                              color="success"
                              dark
                              v-bind="attrs"
                              v-on="on"
                            >
                              mdi-help-circle-outline
                            </v-icon>
                          </template>
                          <span>
                            {{ tooltip.email }}
                          </span>
                        </v-tooltip>
                      </template>
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
                    {{ email }}
                    {{
                      'erhalten. Bitte guck in dein Postfach und benutze den Link zum einloggen'
                    }}
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-btn color="primary" @click="emailSend = false">
                      <v-icon> mdi-refresh </v-icon>
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
import { validationMixin } from 'vuelidate';
import { email, required } from 'vuelidate/lib/validators';

export default {
  mixins: [validationMixin],

  name: 'Login',
  data: () => ({
    showError: false,
    showSuccess: false,
    emailSend: false,
    timeout: 3000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    isEmailFieldIsLoading: false,
    email: '',
    tooltip: {
      scoutName: 'Dieser Name wird dazu verwendet um deinen.',
      email: 'Für die Kommunikation mit dem Tool.',
      mobileNumber: 'Freiwillig',
      scoutOrganisation: 'Blub',
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
  validations: {
    email: {
      required,
      email,
    },
  },
  computed: {
    emailError() {
      const errors = [];
      if (!this.$v.email.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.email.required && errors.push('E-mail ist erforderkich');

      // eslint-disable-next-line
      !this.$v.email.email && errors.push('Ist keine echte E-Mail-Adresse');
      return errors;
    },
  },
  methods: {
    onEmailTypeInEmailField(e) {
      if (e.keyCode === 13) {
        this.onEmailLoginClick();
      }
      this.log += e.key;
    },

    callLoginPost() {
      return axios.post(`${this.API_URL}auth/login/`, {
        email: this.email,
      });
    },

    onEmailLoginClick() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
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
