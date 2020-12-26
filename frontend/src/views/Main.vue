<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-icon class="mx-4" large> mdi-emoticon </v-icon>
      <v-toolbar-title>Anmelde Tool</v-toolbar-title>
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
        Logout
      </v-btn>
    </v-app-bar>
    <router-view />
    <v-footer color="primary lighten-1" padless absolute>
      <v-row justify="center" no-gutters>
        <v-btn v-for="link in links" :key="link" color="white" text rounded class="my-2">
          {{ link }}
        </v-btn>
        <v-col class="primary lighten py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Anmelde-Tool</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  name: 'Main',
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
  data: () => ({
    links: ['Hauptseite', 'Impressum', 'Kontakt'],
  }),
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'login' });
    },
    getHierarchy() {
      const path = `${process.env.VUE_APP_API}basic/scout-hierarchy/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setHierarchy', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getAgeGroup() {
      const path = `${process.env.VUE_APP_API}basic/age-group/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setAgeGroupMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getHierarchy();
    this.getAgeGroup();
  },
};
</script>

<style scoped></style>
