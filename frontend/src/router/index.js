import Vue from 'vue';
import VueRouter from 'vue-router';
import Main from '../views/Main.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Main',
    component: Main,
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue'),
  },
  {
    path: '/aktion/erstellen',
    name: 'AktionErstellen',
    component: () => import('../views/aktion/create/Main.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
