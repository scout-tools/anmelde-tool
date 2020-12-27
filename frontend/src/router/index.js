import Vue from 'vue';
import VueRouter from 'vue-router';
import CheckTokenMain from '@/views/login/CheckToken.vue';
import EventOverview from '@/views/event/overview/Overview.vue';
import SettingsUser from '@/views/settings/user/Main.vue';
import StatisticOverview from '@/views/statistic/overview/Main.vue';
import RegistrationForm from '@/views/registration/Main.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'login',
    component: () => import('../views/login/Login.vue'),
  },
  {
    path: '/check-token',
    name: 'checkToken',
    component: CheckTokenMain,
  },
  {
    path: '/event/create',
    name: 'createEvent',
    component: () => import('../views/event/create/Main.vue'),
  },
  {
    path: '/event/overview',
    name: 'eventOverview',
    component: EventOverview,
  },
  {
    path: '/settings/user',
    name: 'settingsUser',
    component: SettingsUser,
  },
  {
    path: '/statistic/overview',
    name: 'statisticOverview',
    component: StatisticOverview,
  },
  {
    path: '/registration/form/:id',
    name: 'registrationForm',
    component: RegistrationForm,
    props: true,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
