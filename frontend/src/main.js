import Vue from 'vue';
import Vuelidate from 'vuelidate';
import VueJwtDecode from 'vue-jwt-decode';
import VuetifyMoney from 'vuetify-money';
import VueGoogleCharts from 'vue-google-charts';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);
Vue.use(VuetifyMoney);
Vue.use(VueGoogleCharts);

// eslint-disable-next-line import/prefer-default-export
export const EventBus = new Vue();

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
