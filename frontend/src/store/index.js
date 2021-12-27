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
    ageGroupMapping: [],
    roleMapping: [],
    scoutOrgaLevelMapping: [],
    participantRoleMapping: [],
    eatHabitTypeMapping: [],
    travelTypeTypeMapping: [],
    currentEventParticipants: [],
    currentRegistrationSummary: [],
    currentEventCash: [],
    currentEventKitchen: [],
    currentEventProgram: [],
    dpvAddedLocation: false,
    apiIsDown: false,
    scoutGroupMapping: [],
    myStamm: '',
    myBund: '',
    myScoutname: '',
    registeredTents: [{
      id: 1,
      registration: 1,
      tentType: 1,
      usedByScoutGroups: [1],
    }],
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
  modules: {},
  plugins: [createPersistedState()],
});
