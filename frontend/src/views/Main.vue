<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-btn icon @click="$router.push('main')">
        <v-icon>mdi-home</v-icon>
      </v-btn>
    <v-toolbar-title>BdP-DPV-Anmelde Tool</v-toolbar-title>
      <v-spacer></v-spacer>

      <v-btn icon v-if="isAuthenticated" @click="$router.push({name: 'eventOverview'})">
        <v-icon>mdi-view-list</v-icon>
      </v-btn>

      <v-btn icon v-if="isAuthenticated" @click="$router.push({name: 'createEvent'})">
        <v-icon>mdi-calendar-plus</v-icon>
      </v-btn>

      <v-spacer/>
      <v-btn
        outlined
        v-if="!isAuthenticated"
        dark
        to="/login">
        Zugangs E-Mail Anfordern
      </v-btn>
      <v-btn
        v-if="isAuthenticated"
        outlined
        dark
        to="/logout">
        Logout
      </v-btn>
    </v-app-bar>
    <router-view/>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Main',
  computed: {
    ...mapGetters([
      'isAuthenticated',
    ]),
  },
};
</script>

<style scoped>

</style>
