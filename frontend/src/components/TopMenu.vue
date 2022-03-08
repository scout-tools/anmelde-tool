<template>
  <v-app-bar app color="primary" dark absolute>
    <v-tabs
      background-color="primary"
      v-model="tab"
      centered
      dark
      icons-and-text
    >
      <v-tab>
        <router-link to="/">
          <img
            :src="logoPath"
            height="55"
            alt="Logo"
            class="logo-img mx-2 mt-2"
          />
        </router-link>
      </v-tab>

      <v-spacer></v-spacer>
      <v-tab :to="{ name: 'eventOverview' }" v-if="isAuth">
        Meine Anmeldungen
        <v-icon>mdi-view-list</v-icon>
      </v-tab>
      <v-tab :to="{ name: 'eventPlaner' }" v-if="isAuth">
        Meine Fahrten
        <v-icon>mdi-account-key</v-icon>
      </v-tab>
      <v-tab :to="{ name: 'dataOverview' }" v-if="isAuth">
        Auswertungen
        <v-icon>mdi-chart-bar</v-icon>
      </v-tab>
      <v-spacer></v-spacer>
      <v-tab :to="{ name: 'settingsOverview' }" v-if="isAuth">
        Mein Profil
        <v-icon>mdi-account-circle</v-icon>
      </v-tab>
      <v-tab v-if="!isAuth">
        <v-btn color="success" elevation="2" @click="onLoginClicked">
          Login
        </v-btn>
      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex';
import authMixin from '@/mixins/authMixin';

export default {
  name: 'TopMenu',
  mixins: [authMixin],
  data: () => ({
    tab: null,
  }),
  computed: {
    ...mapGetters(['theme', 'userinfo', 'getUserName']),
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require(`@/assets/${this.theme}/logo-dev.png`); // eslint-disable-line
      }
      return require(`@/assets/${this.theme}/logo.png`); // eslint-disable-line
    },
  },
  methods: {
    onLoginClicked() {
      this.$keycloak.login();
    },
  },
};
</script>
