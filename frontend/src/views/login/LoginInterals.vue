<template>
  <div
    class="bg"
    :style="{
      'background-image':
        'url(' + require(`@/assets/${this.theme}/image2.jpg`) + ')',
    }"
  >
    <v-container fill-height fluid>
      <v-row align="center" justify="center">
        <v-col>
          <v-card
            max-width="500px"
            min-width="350px"
            class="mx-auto my-12"
            color="rgb(255, 255, 255, 0.9)"
          >
            <v-card-title class="text-center justify-center py-6">
              Planungsjurte
            </v-card-title>
            <v-card-text class="mt-5">
              <v-subheader>
                Hier kannst du dich einloggen falls du ein Lager
                organisiertst und deine Daten abrufen willst.
              </v-subheader>
              <v-form>
                <v-container v-if="!emailSend">
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="username"
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
                              {{ tooltip.username }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="password"
                        label="Dein Passwort"
                        prepend-icon="mdi-lock"
                        :error-messages="passwordError"
                        v-on:keyup="onEmailTypeInEmailField"
                        type="password"
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
                              {{ tooltip.password }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                  </v-row>
                  <v-spacer />
                  <v-btn color="primary" @click="onPasswordLoginClick">
                    Einloggen
                  </v-btn>
                </v-container>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
  </div>
</template>

<script>
import axios from 'axios';
import { validationMixin } from 'vuelidate';
import { email, required } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';

export default {
  name: 'Login',
  mixins: [validationMixin],
  data: () => ({
    showError: false,
    showSuccess: false,
    emailSend: false,
    timeout: 3000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    isEmailFieldIsLoading: false,
    username: '',
    password: '',
    tooltip: {
      username: 'Dieser Name wird dazu verwendet um deinen.',
      password: 'Für die Kommunikation mit dem Tool.',
    },
    tab: null,
  }),
  validations: {
    username: {
      required,
      email,
    },
    password: {
      required,
    },
  },
  computed: {
    ...mapGetters(['theme']),
    emailError() {
      const errors = [];
      if (!this.$v.username.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.username.required && errors.push('E-mail ist erforderlich');

      // eslint-disable-next-line
      !this.$v.username.email && errors.push('Ist keine echte E-Mail-Adresse');
      return errors;
    },
    passwordError() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.password.required && errors.push('Password ist erforderlich');

      return errors;
    },
  },
  methods: {
    onEmailTypeInEmailField(e) {
      if (e.keyCode === 13) {
        this.onPasswordLoginClick();
      }
      this.log += e.key;
    },

    callTokenPost() {
      return axios.post(`${this.API_URL}auth/token/`, {
        username: this.username,
        password: this.password,
      });
    },

    onEmailLoginClick() {
      this.handleLoginRequest();
    },

    onPasswordLoginClick() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.isEmailFieldIsLoading = true;
      this.handlePasswordLoginRequest();
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

    onSuccessfulEmailSent() {
      this.showSuccess = true;
    },
    onSuccessfulLogin() {
      this.$router.push({ name: 'eventOverview' });
    },
  },
};
</script>
