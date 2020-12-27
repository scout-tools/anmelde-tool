import Vue from 'vue';
import Vuelidate from 'vuelidate';
import VueJwtDecode from 'vue-jwt-decode';
import VuetifyMoney from 'vuetify-money';

import App from './App.vue';
import router from './router';
import store from './store';
import vuetify from './plugins/vuetify';
import 'material-design-icons-iconfont/dist/material-design-icons.css';

Vue.config.productionTip = false;

Vue.use(Vuelidate);
Vue.use(VueJwtDecode);
Vue.use(VuetifyMoney);

new Vue({
  router,
  store,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
