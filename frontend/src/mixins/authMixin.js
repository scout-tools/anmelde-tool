export default {
  computed: {
    isAuth() {
      if (this.$keycloak !== null) {
        return this.$keycloak.authenticated;
      }
      return true;
    },
  },
  methods: {
    logout() {
      this.$keycloak.logoutFn();
      this.$store.commit('clearTokens');
      this.$store.commit('clearUserinfo');
      this.$router.push({ name: 'landing' });
    },
  },
};
