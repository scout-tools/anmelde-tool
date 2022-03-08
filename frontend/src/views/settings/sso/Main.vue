<template>
  <v-card flat>
    <v-card-title class="text-center justify-center py-6">
      Hier kannst du deine Einstellungen anpassen.
    </v-card-title>
    <v-container>
      <v-row>
        <v-btn color="secondary" dark @click="goToIdm">
          <v-icon left>mdi-open-in-new</v-icon>
          Zum DPV-Account
        </v-btn>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    keycloakUrl: process.env.VUE_APP_KEYCLOAK_URL,
    keycloakRealm: process.env.VUE_APP_KEYCLOAK_REALM,
    keycloakClientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,
  }),
  methods: {
    goToIdm() {
      const link = `${this.keycloakUrl}/realms/${this.keycloakRealm}/account/`;
      window.open(link, '_blank');
    },
  },
};
</script>

<style>
</style>
