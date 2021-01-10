<template>
  <v-app-bar app color="primary" dark>
    <router-link to="/">
      <img
        src="@/assets/logo_bdp_dpv.svg"
        height="40"
        alt="Logo"
        class="logo-img mx-2"
      />
    </router-link>
    <v-spacer v-if="!$vuetify.breakpoint.mobile"></v-spacer>

    <v-tabs background-color="primary" centered dark icons-and-text>
      <v-tabs-slider></v-tabs-slider>
      <v-spacer />
      <v-tab
        v-if="isAuthenticated"
        @click="$router.push({ name: 'eventOverview' })"
      >
        Lager
        <v-icon>mdi-view-list</v-icon>
      </v-tab>

      <v-tab
        v-if="isAuthenticated && !isSimpleUser"
        @click="$router.push({ name: 'createEvent' })"
      >
        Neues Lager
        <v-icon>mdi-calendar-plus</v-icon>
      </v-tab>
      <v-spacer />
      <v-tab
        v-if="isAuthenticated"
        @click="$router.push({ name: 'settingsUser' })"
      >
        Einstellungen
        <v-icon>mdi-tools</v-icon>
      </v-tab>
      <v-tab
        v-if="isAuthenticated"
        @click="onLogoutClicked"
      >
        {{ logoutText }}
        <v-icon>mdi-logout-variant</v-icon>
      </v-tab>
    </v-tabs>
  </v-app-bar>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'HelloWorld',

  data: () => ({}),
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
    logoutText() {
      if (this.$vuetify.breakpoint.mobile) {
        return '';
      }
      return 'Logout';
    },
  },
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'landing' });
    },
  },
};
</script>
