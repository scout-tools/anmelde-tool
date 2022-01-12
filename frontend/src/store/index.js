import Vue from 'vue';
import Vuex from 'vuex';
import VueJwtDecode from 'vue-jwt-decode';
import createPersistedState from 'vuex-persistedstate'; // eslint-disable-line
import createEvent from './createEvent';

Vue.use(Vuex);
Vue.use(VueJwtDecode);

export default new Vuex.Store({
  state: {
    accessToken: null,
    refreshToken: null,
    apiIsDown: false,
    userinfo: {
      fahrtenname: '',
      stamm: '',
      bund: '',
    },
  },
  getters: {
    userinfo(state) {
      return state.userinfo;
    },
    getJwtData(state) {
      if (state.accessToken) {
        return VueJwtDecode.decode(state.accessToken);
      }
      return {};
    },
    isAuthenticated(state) {
      return !!state.accessToken;
    },
    apiIsDown(state) {
      return state.apiIsDown;
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
    setUserinfo(state, userinfo) {
      state.userinfo = userinfo;
    },
    clearUserinfo(state) {
      state.userinfo = {
        fahrtenname: '',
        stamm: '',
        bund: '',
      };
    },
    apiIsDown(state, status) {
      state.apiIsDown = status;
    },
  },
  actions: {},
  modules: {
    createEvent,
  },
  plugins: [createPersistedState()],
});
