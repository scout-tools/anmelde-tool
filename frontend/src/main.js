import Vue from 'vue';
import VueJwtDecode from 'vue-jwt-decode';
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
import moment from 'moment';
import Vuelidate from 'vuelidate';
import { LMap, LMarker, LTileLayer } from 'vue2-leaflet';
import { Icon } from 'leaflet';
import VueKeycloakJs from '@dsb-norge/vue-keycloak-js';
import vuetifyMoney from 'vuetify-money';
import CKEditor from '@ckeditor/ckeditor5-vue2';
import VueMask from 'v-mask';
import VueGoogleCharts from 'vue-google-charts';
import VueApexCharts from 'vue-apexcharts';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import keycl from './auth/keycloak';
import auth from './auth';
import 'leaflet/dist/leaflet.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

require('moment/locale/de');

Vue.use(VueGoogleCharts);

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);

Vue.use(require('vue-moment'), {
  moment,
});

Vue.use(VueMask);

Vue.use(VueApexCharts);

Vue.use(CKEditor);

Vue.use(VueLodash, { lodash });
Vue.use(vuetifyMoney);

auth.interceptorsSetup(store, router);

Vue.component('apexchart', VueApexCharts);
Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);

delete Icon.Default.prototype._getIconUrl; //eslint-disable-line
Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'), //eslint-disable-line
  iconUrl: require('leaflet/dist/images/marker-icon.png'), //eslint-disable-line
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'), //eslint-disable-line
});

Vue.prototype.moment = moment;

Vue.use(VueKeycloakJs, {
  init: {
    // Use 'login-required' to always require authentication
    // If using 'login-required', there is no need for the router guards in router.js
    onLoad: 'check-sso',
    checkLoginIframe: false,
    // silentCheckSsoRedirectUri: `${window.location.origin}/silent-check-sso.html`,
  },

  config: {
    url: process.env.VUE_APP_KEYCLOAK_URL,
    realm: process.env.VUE_APP_KEYCLOAK_REALM,
    clientId: process.env.VUE_APP_KEYCLOAK_CLIENT_ID,
    // onLoad: 'check-sso',
    // checkLoginIframe: false,
  },
  onReady(keycloak) {
    store.commit('setTokens', keycloak.token, keycloak.refreshToken);
    keycloak
      .loadUserInfo()
      .then((userInfo) => {
        store.commit('setUserinfo', userInfo);

        keycl.checkPersonalData();
        keycl.setRefreshInterval(keycloak);
        if (router.history.current.name === 'landing') {
          router.push({ name: 'eventOverview' });
        }
      })
      .catch((err) => {
        console.log(err);
        router.push({ name: 'landing' });
      });
  },
});

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
