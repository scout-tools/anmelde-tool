export default {
  computed: {
    isAuth() {
      if (this.$keycloak !== null) {
        return this.$keycloak.authenticated;
      }
      return true;
    },
  },
  data: () => ({
    keycloakUrl: process.env.VUE_APP_KEYCLOAK_URL,
    keycloakRealm: process.env.VUE_APP_KEYCLOAK_REALM,
    keycloakClientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,
  }),
  methods: {
    logout() {
      this.$store.commit('clearTokens');
      this.$store.commit('clearUserinfo');
      const link = `${this.keycloakUrl}/realms/${this.keycloakRealm}/protocol/openid-connect/logout`;
      window.open(link, '_self');
      // this.$keycloak.logoutFn();
      // this.$router.push({ name: 'landing' });
    },
  },
};
