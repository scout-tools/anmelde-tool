<template>
  <v-container>
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
          <v-btn depressed color="secondary" elevation="2" @click="onLoginClicked" v-if="!isAuth">
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
                    <v-btn class="ma-5 text-center" large dark @click="onLogoutClicked">
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

export default {
  name: 'TopMenu',
  data: () => ({
  }),
  computed: {
    ...mapGetters(['userinfo']),
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
      if (this.$keycloak !== null) {
        return this.$keycloak.authenticated;
      }
      return true;
    },
  },
  methods: {
    onLogoutClicked() {
      this.$keycloak.logoutFn();

      this.$store.commit('clearTokens');
      this.$store.commit('clearUserinfo');

      this.$router.push({ name: 'landing' });
    },
    onLoginClicked() {
      this.$keycloak.login();
    },
    goToIdm() { // external keycloak user settings page
      const link = `${this.keycloakUrl}/realms/${this.keycloakRealm}/account/`;
      window.open(link, '_blank');
    },
  },
};
</script>
