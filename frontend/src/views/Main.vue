<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn icon @click="$router.push({ name: 'login' });">
        <v-icon>mdi-home</v-icon>
      </v-btn>
      <v-toolbar-title>BdP-DPV-Anmelde Tool</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn
        icon
        v-if="isAuthenticated"
        @click="$router.push({ name: 'eventOverview' })"
      >
        <v-icon>mdi-view-list</v-icon>
      </v-btn>

      <v-btn
        icon
        v-if="isAuthenticated"
        @click="$router.push({ name: 'createEvent' })"
      >
        <v-icon>mdi-calendar-plus</v-icon>
      </v-btn>

      <v-spacer />
      <v-btn v-if="isAuthenticated" outlined dark @click="onLogoutClicked">
        Logout
      </v-btn>
    </v-app-bar>
    <router-view />
    <v-footer color="primary lighten-1" padless absolute>
      <v-row justify="center" no-gutters>
        <v-btn
          v-for="link in links"
          :key="link"
          color="white"
          text
          rounded
          class="my-2"
        >
          {{ link }}
        </v-btn>
        <v-col class="primary lighten py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Main',
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data: () => ({
    links: ['Hauptseite', 'Impressum', 'Kontakt'],
  }),
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'login' });
    },
  },
};
</script>

<style scoped>
</style>
