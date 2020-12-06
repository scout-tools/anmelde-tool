import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    accessToken: null,
    refreshToken: null,
    currentUser: null,
  },
  getters: {
    getUsername(state) {
      return state.currentUser;
    },
    isAuthenticated(state) {
      return !!state.accessToken;
    },
  },
  mutations: {
    setTokens(state, access, refresh) {
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    setCurrentUser(state, user) {
      state.currentUser = user;
    },
  },
  actions: {
  },
  modules: {
  },
});
