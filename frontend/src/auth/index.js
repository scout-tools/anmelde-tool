import axios from 'axios';
import Vue from 'vue';

export default {
  user: {
    authenticated: false,
  },

  interceptorsSetup() {
    axios.interceptors.request.use(
      async (config) => {
        const token = await this.getToken();
        if (Vue.prototype.$keycloak.authenticated) {
          // eslint-disable-next-line no-param-reassign
          config.headers.Authorization = token;
        }
        return config;
      },
      (err) => Promise.reject(err),
    );

    // axios.interceptors.response.use((response) => {
    //   store.commit('apiIsDown', false);
    //   return response;
    // }, (error) => {
    //   if (error && error.response === undefined) {
    //     store.commit('apiIsDown', true);
    //   }
    //
    //   if (error.response.status === 401) {
    //     if (error.response.data.detail !==
    //     'No active account found with the given credentials') {
    //       store.commit('clearTokens');
    //       window.location.href = '/';
    //     }
    //   }
    //   return Promise.reject(error);
    // });
  },
  getToken() {
    return new Promise((resolve) => {
      if (Vue.prototype.$keycloak.authenticated) {
        resolve(`Bearer ${Vue.prototype.$keycloak.token}`);
      } else {
        setTimeout(() => {
          resolve(`Bearer ${Vue.prototype.$keycloak.token}`);
        }, 500);
      }
    });
  },
};
