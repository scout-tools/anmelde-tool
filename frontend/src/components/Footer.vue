<template>
  <div>
    <v-footer color="primary lighten-1" padless>
      <v-row justify="center" no-gutters>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'impressum' })"
        >
          <v-icon fab color="white" class="mr-1">
            mdi-card-text-outline
          </v-icon>
          Impressum
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'contact' })"
        >
          <v-icon fab color="white" class="mr-1">
            mdi-account-box
          </v-icon>
          Kontakt
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'contact' })"
        >
          <v-icon fab color="white" class="mr-1">
            mdi-fingerprint
          </v-icon>
          Datenschutz

        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'loginInterals' })"
        >
          <v-icon fab color="white" class="mr-1">
            mdi-chess-king
          </v-icon>
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
          <v-icon fab color="white" class="mr-1">
            mdi-logout-variant
          </v-icon>
          Logout
        </v-btn>
        <!-- <v-col class="primary lighten py-1 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Anmelde-Tool</strong>
        </v-col> -->
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
