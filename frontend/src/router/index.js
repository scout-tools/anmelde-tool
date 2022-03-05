import Vue from 'vue';
import VueRouter from 'vue-router';
import SettingsUser from '@/views/settings/user/Main.vue';
import CheckTokenMain from '@/views/login/CheckToken.vue';
import EventOverview from '@/views/event/overview/Overview.vue';
import EventAdminOverview from '@/views/event/admin/Overview.vue';
import MasterDataOverview from '@/views/event/data/Overview.vue';
import SettingsOverview from '@/views/settings/Main.vue';
import SettingsConfig from '@/views/settings/config/Main.vue';
// import StatisticOverview from '@/views/statistic/Main.vue';
// import RegistrationForm from '@/views/registration/Main.vue';
// import RegistrationCreate from '@/views/registration/create/Main.vue';
import LandingPage from '@/views/landingPage/Main.vue';
import Impressum from '@/views/footer/Impressum.vue';
import Datenschutz from '@/views/footer/Datenschutz.vue';
import EventPlaner from '@/views/eventPlaner/Main.vue';
import PlanEvent from '@/views/eventPlaner/create/Main.vue';
// import CheckTokenMain from '@/views/login/CheckToken.vue';
// import StatisticOverview from '@/views/statistic/Main.vue';
// import RegistrationForm from '@/views/registration/Main.vue';
// import RegistrationCreate from '@/views/registration/create/Main.vue';
// import CreateEvent from '@/views/event/create/Main.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
  },
  {
    path: '/eventplaner',
    name: 'eventPlaner',
    component: EventPlaner,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/planevent/:id/:step?',
    name: 'planEvent',
    component: PlanEvent,
    meta: {
      requiresAuth: true,
    },
  }, {
    path: '/check-token',
    name: 'checkToken',
    component: CheckTokenMain,
  },
  // {
  //   path: '/event/create',
  //   name: 'createEvent',
  //   component: CreateEvent,
  // },
  // {
  //   path: '/event/update/:id',
  //   name: 'updateEvent',
  //   component: CreateEvent,
  //   props: true,
  // },
  // {
  //   path: '/check-token',
  //   name: 'checkToken',
  //   component: CheckTokenMain,
  // },
  // {
  //   path: '/event/create/:id',
  //   name: 'createEvent',
  //   component: CreateEvent,
  //   props: true,
  // },
  {
    path: '/event/overview',
    name: 'eventOverview',
    component: EventOverview,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/event/adminOverview',
    name: 'eventAdminOverview',
    component: EventAdminOverview,
  },
  {
    path: '/data/overview',
    name: 'dataOverview',
    component: MasterDataOverview,
  },
  {
    path: '/settings/overview',
    name: 'settingsOverview',
    component: SettingsOverview,
  },
  {
    path: '/settings/user',
    name: 'settingsUser',
    component: SettingsUser,
    meta: {
      requiresAuth: true,
    },
  },
  // {
  //   path: '/statistic/:id',
  //   name: 'statisticOverview',
  //   component: StatisticOverview,
  //   props: true,
  // },
  // {
  //   path: '/registration/form/:id',
  //   name: 'registrationForm',
  //   component: RegistrationForm,
  //   props: true,
  // },
  // {
  //   path: '/registration/create/:id',
  //   name: 'registrationCreate',
  //   component: RegistrationCreate,
  //   props: true,
  // },
  {
    path: '/settings/config',
    name: 'settingsConfig',
    component: SettingsConfig,
  },
  // {
  //   path: '/statistic/:id',
  //   name: 'statisticOverview',
  //   component: StatisticOverview,
  //   props: true,
  // },
  // {
  //   path: '/registration/form/:id',
  //   name: 'registrationForm',
  //   component: RegistrationForm,
  //   props: true,
  // },
  // {
  //   path: '/registration/create/:id',
  //   name: 'registrationCreate',
  //   component: RegistrationCreate,
  //   props: true,
  // },
  {
    path: '/impressum',
    name: 'impressum',
    component: Impressum,
  },
  {
    path: '/datenschutz',
    name: 'datenschutz',
    component: Datenschutz,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

function sleep(ms) {
  // eslint-disable-next-line no-promise-executor-return
  return new Promise((resolve) => setTimeout(resolve, ms));
}

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // We wait for Keycloak init, then we can call all methods safely
    while (router.app.$keycloak.createLoginUrl === null) {
      // eslint-disable-next-line no-await-in-loop
      await sleep(100);
    }
    if (router.app.$keycloak.authenticated) {
      next();
    } else {
      const loginUrl = router.app.$keycloak.createLoginUrl();
      window.location.replace(loginUrl);
    }
  } else {
    next();
  }
});

export default router;
