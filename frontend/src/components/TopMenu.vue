<template>
  <v-container v-if="loadedData">
    <v-app-bar app color="primary" dark absolute>
      <v-tabs background-color="primary" centered dark icons-and-text>
        <v-tab>
          <router-link to="/">
            <img
              :src="logoPath"
              height="55"
              alt="Logo"
              class="logo-img mx-2"/>
          </router-link>
        </v-tab>
        <v-spacer/>
        <v-tab v-if="isAuth" @click="$router.push({ name: 'eventOverview' })">
          Fahrten
          <v-icon>mdi-view-list</v-icon>
        </v-tab>
        <v-tab v-if="isAuth" @click="$router.push({ name: 'eventPlanning' })">
          Eventplaner
          <v-icon>mdi-view-list</v-icon>
        </v-tab>
        <v-spacer/>
        <v-card-actions class="justify-center">
          <v-btn depressed color="secondary" elevation="2" @click="login" v-if="!isAuth">
            Login
          </v-btn>
          <v-menu bottom offset-y v-else>
            <template v-slot:activator="{ on, attrs }">
              <v-tab
                text
                class="align-self-center mr-4"
                v-bind="attrs"
                v-on="on"
                icon
                fab
                dark
                circle
                x-large>
                Profil
                <v-icon x-large>mdi-account-circle</v-icon>
              </v-tab>
            </template>
            <v-card>
              <v-card-title class="justify-center">
                {{ userName }}
              </v-card-title>
              <v-card-subtitle class="text-center">
                Stamm: {{ userinfo.stamm }} ({{ userinfo.bund }})
              </v-card-subtitle>
              <v-divider></v-divider>
              <v-card-actions>
                <v-list class="justify-center">
                  <v-list-item class="justify-center">
                    <v-btn color="secondary" small dark depressed @click="goToIdm">
                      Edit DPV IDM Profil
                    </v-btn>
                  </v-list-item>
                  <v-list-item class="justify-center">
                    <v-btn small depressed
                           color="secondary"
                           @click="$router.push({ name: 'settingsUser' })">
                      Edit Anmelde-Tool Profil
                    </v-btn>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item class="justify-center">
                    <v-btn class="ma-5 text-center" large dark @click="logout">
                      Logout
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-card-actions>
            </v-card>
          </v-menu>

        </v-card-actions>
      </v-tabs>
    </v-app-bar>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import Keycloak from 'keycloak-js';
import axios from 'axios';

export default {
  name: 'TopMenu',
  data: () => ({
    fav: true,
    menu: false,
    message: false,
    hints: true,
    API_URL: process.env.VUE_APP_API,
    userinfo: {
      fahrtenname: '',
      stamm: '',
      bund: '',
    },
    keycloakUrl: process.env.VUE_APP_KEYCLOAK_URL,
    keycloakRealm: process.env.VUE_APP_KEYCLOAK_REALM,
    keycloakClientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,

    keycloak: null,
    loadedData: false,
  }),
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require('../assets/dpvgold/dpv-gold-logo-test-simple.png'); // eslint-disable-line
      }
      return require('../assets/dpvgold/dpv-gold-logo-white_simple.png'); // eslint-disable-line
    },
    userName() {
      if (this.userinfo) {
        if (this.userinfo.fahrtenname && this.userinfo.fahrtenname.length > 0) {
          return this.userinfo.fahrtenname;
        }
        return this.userinfo.name;
      }
      return '';
    },
    isAuth() {
      if (this.keycloak !== null) {
        return this.keycloak.authenticated;
      }
      return true;
    },
  },
  methods: {
    afterAuth() {
      this.$store.commit('setTokens',
        this.keycloak.token,
        this.keycloak.refreshToken);
      this.keycloak.loadUserInfo()
        .then((userInfo) => {
          this.userinfo = userInfo;
        });
    },
    checkUser() {
      const path = `${this.API_URL}/auth/personal-data-check/`;
      axios.get(path)
        .then((res) => {
          console.log(res);
          if (res.status === 426) {
            this.router.push({ name: 'settingsUser' });
          }
        })
        .catch((err) => {
          console.log(err);
          if (err.response.status === 426) {
            this.$router.push({ name: 'settingsUser' });
          }
        });
    },
    login() {
      this.keycloak.login()
        .then((auth) => {
          if (auth) {
            this.afterAuth();
            this.refreshToken();
            this.checkUser();
          }
        })
        .catch((error) => {
          console.error('Authenticated Failed: ', error);
          this.logout();
        })
        .finally(() => {
          this.loadedData = true;
        });
    },
    logout() {
      this.keycloak.logout();
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'landing' });
      this.userinfo = null;
    },
    refreshToken() {
      if (this.isAuthenticated) {
        setInterval(() => {
          this.keycloak.updateToken(70)
            .then((refreshed) => {
              if (refreshed) {
                console.log(`Token refreshed ${refreshed}`);
              } else {
                console.log(`Token not refreshed, valid for ${
                  Math.round(this.keycloak.tokenParsed.exp + this.keycloak.timeSkew - new Date().getTime() / 1000)} seconds`);
              }
            })
            .catch(() => {
              console.log('Failed to refresh token');
            });
        }, 6000);
      }
    },
    goToIdm() {
      const link = `${this.keycloakUrl}/realms/${this.keycloakRealm}/account/`;
      window.open(link, '_blank');
    },
  },
  mounted() {
    const initOptions = {
      url: this.keycloakUrl,
      realm: this.keycloakRealm,
      clientId: this.keycloakClientId,
      onLoad: 'check-sso',
      checkLoginIframe: false,
    };
    this.keycloak = Keycloak(initOptions);

    this.keycloak.init({
      onLoad: initOptions.onLoad,
      checkLoginIframe: initOptions.checkLoginIframe,
    })
      .then((auth) => {
        console.log(auth);
        if (auth) {
          console.log('Authenticated');
          this.afterAuth();
          this.refreshToken();
          this.checkUser();
        }
      })
      .catch((error) => {
        console.error('Authenticated Failed: ', error);
        this.logout();
      })
      .finally(() => {
        this.loadedData = true;
      });
  },
};
</script>
