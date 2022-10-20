import Vue from 'vue';
import VueRouter from 'vue-router';
import SettingsUser from '@/views/settings/user/Main.vue';
import EventOverview from '@/views/event/overview/Overview.vue';

import MasterDataOverview from '@/views/masterData/Main.vue';

import StatisticMain from '@/views/statistic/Main.vue';
import StatisticOverview from '@/views/statistic/overview/Main.vue';

import SettingsOverview from '@/views/settings/Main.vue';
import SettingsConfig from '@/views/settings/config/Main.vue';
import SettingsPerson from '@/views/settings/person/Main.vue';
import SettingsSso from '@/views/settings/sso/Main.vue';

import LandingPage from '@/views/landingPage/Main.vue';
import RedirectKeycloak from '@/views/landingPage/RedirectKeycloak.vue';
import Impressum from '@/views/footer/Impressum.vue';
import Datenschutz from '@/views/footer/Datenschutz.vue';
import FAQ from '@/views/footer/FAQ.vue';
import EventPlaner from '@/views/eventPlaner/Main.vue';
import PlanEvent from '@/views/eventPlaner/create/Main.vue';

import MessageList from '@/views/masterData/message/MessageList.vue';
import ThemeList from '@/views/masterData/theme/ThemeList.vue';

import registrationEdit from '@/views/registration/CreateUpdateContainer.vue';
import registrationCompleted from '@/views/registration/Completed.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'landing',
    component: LandingPage,
  },
  {
    path: '/redirect-keycloak',
    name: 'redirectKeycloak',
    component: RedirectKeycloak,
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
  },
  {
    path: '/event/overview',
    name: 'eventOverview',
    component: EventOverview,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/masterData',
    name: 'masterDataOverview',
    component: MasterDataOverview,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: 'message-list',
        component: MessageList,
      },
      {
        path: 'theme-list',
        component: ThemeList,
      },
    ],
  },
  {
    path: '/settings',
    name: 'settingsOverview',
    component: SettingsOverview,
    redirect: { name: 'settingsUser' },
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        name: 'settingsUser',
        path: 'user',
        component: SettingsUser,
      },
      {
        path: 'person',
        component: SettingsPerson,
      },
      {
        path: 'config',
        component: SettingsConfig,
      },
      {
        path: 'sso',
        component: SettingsSso,
      },
    ],
  },
  {
    path: '/registration/edit/:id',
    name: 'registrationEdit',
    component: registrationEdit,
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/registration/completed/:id',
    name: 'registrationCompleted',
    component: registrationCompleted,
    props: true,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/statistic/:id',
    name: 'statisticOverview',
    component: StatisticMain,
    meta: {
      requiresAuth: true,
    },
    children: [
      {
        path: 'overview',
        name: 'statistic-overview',
        component: StatisticOverview,
      },
    ],
  },
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
  {
    path: '/faq',
    name: 'faq',
    component: FAQ,
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
