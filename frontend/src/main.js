import Vue from 'vue';
import Vuelidate from 'vuelidate';
import VueJwtDecode from 'vue-jwt-decode';
import VuetifyMoney from 'vuetify-money';
import VueGoogleCharts from 'vue-google-charts';
import VueLodash from 'vue-lodash';
import lodash from 'lodash';
import AsyncComputed from 'vue-async-computed';
import moment from 'moment';
import { LMap, LTileLayer, LMarker } from 'vue2-leaflet';
import 'leaflet/dist/leaflet.css';
import { Icon } from 'leaflet';
import CKEditor from '@ckeditor/ckeditor5-vue2';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import auth from './auth';

import 'material-design-icons-iconfont/dist/material-design-icons.css';

require('moment/locale/de');

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);
Vue.use(VuetifyMoney);
Vue.use(VueGoogleCharts);
Vue.use(AsyncComputed);

Vue.use(require('vue-moment'), {
  moment,
});

Vue.use(CKEditor);

Vue.use(VueLodash, { lodash });

Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);

auth.interceptorsSetup(store, router);

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
