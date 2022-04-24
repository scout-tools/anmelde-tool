<template>
  <v-app-bar app color="primary" dark absolute>
    <div class="my-10" style="color: red" />
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
      <v-tab
        :disabled="accountIncomplete"
        :to="{ name: 'eventOverview' }"
        v-if="isAuth"
      >
        Meine Anmeldungen
        <v-icon>mdi-view-list</v-icon>
      </v-tab>
      <v-tab
        :disabled="accountIncomplete"
        :to="{ name: 'eventPlaner' }"
        v-if="isAuth"
      >
        Meine Fahrten
        <v-icon>mdi-account-key</v-icon>
      </v-tab>
      <v-tab
        :disabled="accountIncomplete"
        :to="{ name: 'masterDataOverview' }"
        v-if="userinfo && isTeam"
      >
        Stammdaten
        <v-icon>mdi-tools</v-icon>
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
    ...mapGetters(['theme', 'userinfo', 'getUserName', 'accountIncomplete']),
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require(`@/assets/${this.theme}/logo-dev.png`); // eslint-disable-line
      }
      return require(`@/assets/${this.theme}/logo.png`); // eslint-disable-line
    },
    isTeam() {
      return this.userinfo.roles.includes('anmelde_tool_team');
    },
  },
  methods: {
    onLoginClicked() {
      this.$keycloak.login();
    },
  },
};
</script>
