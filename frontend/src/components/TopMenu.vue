<template>
  <v-container>
    <v-app-bar app color="primary" dark absolute>
      <v-tabs background-color="primary" centered dark icons-and-text>
        <v-tab>
          <router-link to="/">
            <img
              :src="getLogoPath"
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
        <v-tab v-if="isAuth" @click="$router.push({ name: 'eventPlaner' })">
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
                {{ getUserName }}
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
import authMixin from '@/mixins/authMixin';
import basicInfoMixin from '@/mixins/basicInfoMixin';

export default {
  name: 'TopMenu',
  mixins: [authMixin, basicInfoMixin],
  computed: {
    ...mapGetters(['userinfo']),
    isAuth() {
      if (this.$keycloak !== null) {
        return this.$keycloak.authenticated;
      }
      return true;
    },
  },
  methods: {
    onLogoutClicked() {
      this.logout();
    },
    onLoginClicked() {
      this.$keycloak.login();
    },
    goToIdm() { // external keycloak user settings page
      const link = `${process.env.VUE_APP_KEYCLOAK_URL}/realms/${process.env.VUE_APP_KEYCLOAK_REALM}/account/`;
      window.open(link, '_blank');
    },
  },
};
</script>
