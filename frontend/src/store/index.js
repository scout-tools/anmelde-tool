import Vue from 'vue';
import Vuex from 'vuex';
import VueJwtDecode from 'vue-jwt-decode';
import createPersistedState from 'vuex-persistedstate'; // eslint-disable-line

Vue.use(Vuex);
Vue.use(VueJwtDecode);

export default new Vuex.Store({
  state: {
    accessToken: null,
    refreshToken: null,
    hierarchy: [],
  },
  getters: {
    getJwtData(state) {
      return VueJwtDecode.decode(state.accessToken);
    },
    isAuthenticated(state) {
      return !!state.accessToken;
    },
    hierarchy(state) {
      return state.hierarchy;
    },
  },
  mutations: {
    setTokens(state, access, refresh) {
      state.accessToken = access;
      state.refreshToken = refresh;
    },
    clearTokens(state) {
      state.accessToken = null;
      state.refreshToken = null;
      state.originalAccessToken = null;
      state.originalRefreshToken = null;
    },
    setHierarchy(state, newHierarchy) {
      state.hierarchy = newHierarchy;
    },
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()],
});
