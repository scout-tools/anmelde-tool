<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="isLoading">
            <v-subheader inset>
              Wir versuchen dich automatisch einzuloggen.
            </v-subheader>
            <div class="text-center">
              <v-progress-circular
                :size="80"
                :width="10"
                color="primary"
                indeterminate
              ></v-progress-circular>
            </div>
          </v-card>
          <v-card v-else>
            <v-toolbar dark color="primary">
              <v-toolbar-title>
                {{ 'Automatischer Login ist fehlgeschlagen' }}
              </v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text class="mt-5">
              <v-subheader inset>
                Gib die Daten aus der E-Mail bitte in das Formular ein.
              </v-subheader>
              <v-form>
                <v-container>
                  <v-row>
                    <v-col cols="12">
                      <v-text-field
                        v-model="username"
                        label="Deine E-Mail Adresse"
                        prepend-icon="mdi-email"
                        :error-messages="emailError"
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
                              {{ 'dsfsF' }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12">
                      <v-text-field
                        v-model="password"
                        label="Dein Logintoken"
                        prepend-icon="mdi-lock"
                        :error-messages="passwordError"
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
                              {{ 'sdas' }}
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
        </v-layout>
      </v-flex>
    </v-row>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
      {{ responseObj }}
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';
import { required, email } from 'vuelidate/lib/validators';

export default {
  name: 'Login',
  data: () => ({
    showError: false,
    emailSend: false,
    timeout: 6000,
    responseObj: null,
    API_URL: process.env.VUE_APP_API,
    isLoading: false,
    username: null,
    password: null,
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
    onPasswordLoginClick() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.onButtonClick();
    },
    onButtonClick() {
      this.isLoading = true;
      axios
        .post(`${this.API_URL}auth/token/`, {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          this.$store.commit(
            'setTokens',
            response.data.access,
            response.data.refresh,
          );
          this.isLoading = false;
          this.onSuccessfulLogin();
        })
        .catch((error) => {
          this.responseObj = error.response.data;
          this.showError = true;
          this.isLoading = false;
        });
    },
    onSuccessfulLogin() {
      this.isLoading = false;
      this.$router.push({ name: 'eventOverview' });
    },
    setDataFromParams() {
      this.username = this.$route.query.username;
      this.password = this.$route.query.password;
    },
  },
  mounted() {
    this.setDataFromParams();
    this.onButtonClick();
  },
};
</script>
