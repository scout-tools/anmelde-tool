<template>
  <v-app-bar app color="primary" dark absolute>
    <v-tabs background-color="primary" v-model="tab" centered dark icons-and-text>
      <v-tab>
        <router-link to="/">
          <img :src="logoPath" height="55" alt="Logo" class="logo-img mx-2" />
        </router-link>
      </v-tab>

      <v-spacer></v-spacer>
      <v-tab
        :to="{ name: 'eventOverview' }"
        v-if="isAuthenticated"
      >
        Meine Anmeldungen
        <v-icon>mdi-view-list</v-icon>
      </v-tab>
      <v-tab
        :to="{ name: 'eventAdminOverview' }"
        v-if="isAuthenticated"
      >
        Meine Fahrten
        <v-icon>mdi-account-key</v-icon>
      </v-tab>
      <v-tab
        :to="{ name: 'dataOverview' }"
        v-if="isAuthenticated && !isSimpleUser"
      >
        Meine Daten
        <v-icon>mdi-chart-bar</v-icon>
      </v-tab>
      <v-spacer></v-spacer>
      <v-tab
        :to="{ name: 'settingsOverview' }"
        v-if="isAuthenticated"
      >
        Mein Profil
        <v-icon>mdi-account-circle</v-icon>
      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex';
// import authMixin from '@/mixins/authMixin';
// import basicInfoMixin from '@/mixins/basicInfoMixin';

export default {
  name: 'TopMenu',

  data: () => ({
    tab: null,
  }),
  computed: {
    ...mapGetters(['isAuthenticated', 'theme']),
    userName() {
      return '';
    },
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require(`@/assets/${this.theme}/logo-dev.png`); // eslint-disable-line
      }
      return require(`@/assets/${this.theme}/logo.png`); // eslint-disable-line
    },
    isSimpleUser() {
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
