import Vue from 'vue';
import Vuex from 'vuex';
import VueJwtDecode from 'vue-jwt-decode';
import createPersistedState from 'vuex-persistedstate'; // eslint-disable-line
import createEvent from './createEvent';
import vuetify from '@/plugins/vuetify';

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
    scoutGroupMapping: [],
    myStamm: '',
    myBund: '',
    myScoutname: '',
    registeredTents: [{
      id: 1, registration: 1, tentType: 1, usedByScoutGroups: [1],
    }],
    preferences: {
      theme: 'default',
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
    scoutGroupMapping(state) {
      return state.scoutGroupMapping;
    },
    registeredTents(state) {
      return state.registeredTents;
    },
    theme(state) {
      return state.preferences.theme;
    },
  },
  mutations: {
    setTheme(state, theme) {
      Vue.set(state.preferences, 'theme', theme);
      vuetify.framework.theme.themes.dark = vuetify.userPreset.theme.themes[theme];
      vuetify.framework.theme.themes.light = vuetify.userPreset.theme.themes[theme];
    },
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
