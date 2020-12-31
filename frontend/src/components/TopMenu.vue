<template>
    <v-app-bar app color="primary" dark>
      <v-btn
        depressed
        color="primary"
        @click="$router.push({ name: 'landing' })"
      >
        <img
          src="@/assets/logo_bdp_dpv.svg"
          height="40"
          alt="Logo"
          class="logo-img mx-2"
        />
        <v-toolbar-title
          v-if="!$vuetify.breakpoint.mobile"
        >Anmelde Tool</v-toolbar-title>
      </v-btn>
      <v-spacer v-if="!$vuetify.breakpoint.mobile"></v-spacer>

            <v-tabs
              background-color="primary"
              centered
              dark
              icons-and-text
            >
              <v-tabs-slider></v-tabs-slider>

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
                Neu
                <v-icon>mdi-calendar-plus</v-icon>
              </v-tab>

              <v-tab
                v-if="isAuthenticated && !isSimpleUser"
                @click="$router.push({ name: 'statisticOverview' })"
              >
                Zahlen
                <v-icon>mdi-chart-bar</v-icon>
              </v-tab>
            </v-tabs>

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
        <v-icon :left="!$vuetify.breakpoint.mobile">
          mdi-logout-variant
        </v-icon>
        {{ logoutText}}
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
      this.$router.push({ name: 'login-internals' });
    },
  },
};
</script>
