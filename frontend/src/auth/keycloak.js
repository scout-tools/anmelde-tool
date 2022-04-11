import axios from 'axios';
import router from '../router';
import store from '../store';

const keycl = {
  checkPersonalData() {
    const path = `${process.env.VUE_APP_API}/auth/personal-data-check/`;
    axios.get(path)
      .then((res) => {
        if (res.status === 426) {
          store.commit('setAccountIncomplete', true);
          router.push({ name: 'settingsOverview' });
        }
      })
      .catch((err) => {
        if (err.response.status === 426) {
          store.commit('setAccountIncomplete', true);
          if (router.history.current.meta.requiresAuth) {
            router.push({ name: 'settingsOverview' });
          }
        }
      });
  },
  setRefreshInterval(keycloak) {
    setInterval(() => {
      keycloak.updateToken(70) // 7 sec
        .then((refreshed) => {
          if (refreshed) {
            console.log(`Token refreshed ${refreshed}`);
          } else {
            console.log(`Token not refreshed, valid for ${
              Math.round(keycloak.tokenParsed.exp + keycloak.timeSkew - new Date().getTime() / 1000)} seconds`);
          }
        })
        .catch(() => {
          console.log('Failed to refresh token');
        });
    }, 6000); // 6 sec
  },
};

export default keycl;
