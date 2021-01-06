import axios from 'axios';

export default {
  user: {
    authenticated: false,
  },

  interceptorsSetup(store) {
    axios.interceptors.request.use((config) => {
      const { accessToken } = store.state;
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`; // eslint-disable-line no-param-reassign
      }
      return config;
    }, (err) => Promise.reject(err));

    axios.interceptors.response.use((response) => {
      store.commit('apiIsDown', false);
      return response;
    }, (error) => {
      if (error && error.response === undefined) {
        store.commit('apiIsDown', true);
      }

      if (error.response.status === 401) {
        if (error.response.data.detail !== 'No active account found with the given credentials') {
          store.commit('clearTokens');
          window.location.href = '/';
        }
      }
      return Promise.reject(error);
    });
  },
};
