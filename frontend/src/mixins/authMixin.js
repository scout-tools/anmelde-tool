export default {
  methods: {
    logout() {
      this.$keycloak.logoutFn();
      this.$store.commit('clearTokens');
      this.$store.commit('clearUserinfo');
      this.$router.push({ name: 'landing' });
    },
  },
};
