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
    ageGroupMapping: [],
    currentEventParticipants: [],
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
    ageGroupMapping(state) {
      return state.ageGroupMapping;
    },
    currentEventParticipants(state) {
      return state.currentEventParticipants;
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
    },
    setHierarchy(state, newHierarchy) {
      state.hierarchy = newHierarchy;
    },
    setAgeGroupMapping(state, newAgeGroup) {
      state.ageGroupMapping = newAgeGroup;
    },
    setCurrentEventParticipants(state, newData) {
      state.currentEventParticipants = newData;
    },
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()],
});
