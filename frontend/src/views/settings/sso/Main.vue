<template>
  <div>
    <v-btn color="secondary" dark @click="goToIdm">
      <v-icon left>mdi-open-in-new</v-icon>
      Zum DPV-Account
    </v-btn>
  </div>
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
