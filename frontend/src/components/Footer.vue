<template>
  <div>
    <v-footer color="primary lighten-1" padless absolute>
      <v-row justify="center" no-gutters>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'impressum' })"
        >
          Impressum
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'contact' })"
        >
          Kontakt
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'contact' })"
        >
          Datenschutz
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'loginInterals' })"
        >
          Planungsjurte
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          v-if="isAuthenticated"
          @click="onLogoutClicked"
        >
          Logout
        </v-btn>
        <v-col class="primary lighten py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Anmelde-Tool</strong>
        </v-col>
      </v-row>
    </v-footer>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data: () => ({
    links: ['Impressum', 'Kontakt', 'Planungsjurte'],
  }),
  methods: {
    onLogoutClicked() {
      this.$store.commit('clearTokens');
      this.$router.push({ name: 'landing' });
    },
  },
};
</script>

<style></style>
