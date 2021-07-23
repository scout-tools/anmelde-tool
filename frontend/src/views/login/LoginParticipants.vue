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
              <p v-if="!emailSend && !isEmailFieldIsLoading">
                Gebe hier deine E-Mail-Adresse an. Den Link zur Anmeldung und
                den Aktionen bekommst du dann per Mail. Für ein erneutes
                Einloggen benutze den Link aus der Mail oder gebe deine E-Mail
                einfach erneut an.
              </p>
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
                <v-row>
                  <v-col cols="5">
                    <v-btn color="primary" @click="onEmailLoginClick">
                      Absenden
                    </v-btn>
                  </v-col>
                  <v-col cols="5"> </v-col>
                </v-row>
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
                <v-divider class="my-5" />
              </v-container>
              <v-expansion-panels
                v-if="emailSend && !isEmailFieldIsLoading"
                flat
              >
                <v-expansion-panel>
                  <v-expansion-panel-header
                    style="background: rgba(200, 54, 54, 0.3)"
                  >
                    Login klappt nicht? (Klicke hier)
                  </v-expansion-panel-header>
                  <v-expansion-panel-content
                    style="background: rgba(200, 54, 54, 0.3)"
                  >
                    <v-btn color="primary" @click="emailSend = false">
                      <v-icon left> mdi-refresh </v-icon>
                      Mit einer anderen E-Mail einloggen
                    </v-btn>
                    <v-container>
                      <p class="my-3">
                        Falls der Login-Button in der E-Mail nicht funktioniert,
                        kannst du hier den Token eingeben und dich einloggen
                      </p>
                      <v-row>
                        <v-col cols="12" sm="8">
                          <v-text-field
                            v-model="token"
                            color="primary"
                            x-large
                            placeholder="'Token aus E-Mail hier eingeben'"
                          >
                            <v-icon left>mdi-key</v-icon>
                            Token aus der E-Mail eingeben
                          </v-text-field>
                        </v-col>
                        <v-col cols="12" sm="3">
                          <v-btn
                            icon
                            outlined
                            @click="
                              $router.push({
                                name: 'checkToken',
                                query: {
                                  username: email,
                                  password: token,
                                },
                              })
                            "
                          >
                            <v-icon> mdi-login </v-icon>
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-divider />
                      <v-row>
                        <v-btn
                          text
                          small
                          class="mb-3"
                          @click="$router.push({ name: 'checkToken' })"
                        >
                          E-Mail Link klappt nicht?
                        </v-btn>
                      </v-row>
                    </v-container>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
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
    token: null,
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
      !this.$v.email.required && errors.push('E-Mail ist erforderlich');

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
