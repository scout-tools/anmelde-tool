import Vue from 'vue';
import VueJwtDecode from 'vue-jwt-decode';
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
import moment from 'moment';
import Vuelidate from 'vuelidate';
import { LMap, LMarker, LTileLayer } from 'vue2-leaflet';
import { Icon } from 'leaflet';
import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import auth from './auth';
import 'leaflet/dist/leaflet.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

const VueMoment = require('vue-moment');

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);
Vue.use(VueMoment);
Vue.use(VueLodash, { lodash });

auth.interceptorsSetup(store, router);

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

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
