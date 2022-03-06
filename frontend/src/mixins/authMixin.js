export default {
  computed: {
    isAuth() {
      if (this.$keycloak !== null) {
        return this.$keycloak.authenticated;
      }
      return true;
    },
  },
};
