<template>
    <v-app-bar app color="primary" dark>
      <v-btn
        depressed
        color="primary"
        @click="$router.push({ name: 'landing' })"
      >
        <v-icon class="mx-4" large> mdi-emoticon </v-icon>
        <v-toolbar-title>Anmelde Tool</v-toolbar-title>
      </v-btn>
      <v-spacer></v-spacer>

      <v-btn
        class="mx-3"
        icon
        large
        v-if="isAuthenticated"
        @click="$router.push({ name: 'eventOverview' })"
      >
        <v-icon>mdi-view-list</v-icon>
      </v-btn>

      <v-btn
        class="mx-3"
        icon
        large
        v-if="isAuthenticated && !isSimpleUser"
        @click="$router.push({ name: 'createEvent' })"
      >
        <v-icon>mdi-calendar-plus</v-icon>
      </v-btn>

      <v-btn
        class="mx-3"
        icon
        large
        v-if="isAuthenticated && !isSimpleUser"
        @click="$router.push({ name: 'statisticOverview' })"
      >
        <v-icon>mdi-chart-bar</v-icon>
      </v-btn>

      <v-spacer />

      <v-btn
        icon
        large
        class="mx-5"
        v-if="isAuthenticated"
        @click="$router.push({ name: 'settingsUser' })"
      >
        <v-icon>mdi-tools </v-icon>
      </v-btn>

      <v-btn v-if="isAuthenticated" outlined dark @click="onLogoutClicked">
        <v-icon left>
          mdi-logout-variant
        </v-icon>
        Logout
      </v-btn>
      <v-btn v-else outlined dark @click="$router.push({ name: 'loginInterals' })">
        <v-icon left>
          mdi-login-variant
        </v-icon>
        Login
      </v-btn>
    </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'HelloWorld',

  data: () => ({
  }),
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    userName() {
      return this.getJwtData.email;
    },
    isSimpleUser() {
      if (this.getJwtData) {
        return !(this.getJwtData.groups.length || this.getJwtData.isStaff);
      }
      return true;
    },
  },
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'login-internals' });
    },
    onLoginClicked() {
      debugger;
    },
  },
};
</script>
