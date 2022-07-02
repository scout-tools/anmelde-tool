import axios from 'axios';

export default {
  // eslint-disable-line
  methods: {
    async getServiceById(id, modulePath) {
      const path = `${process.env.VUE_APP_API}${modulePath}${id}/`;
      const response = await axios.get(path);

      return response.data;
    },
    getSimpleService(modulePath, params) {
      const path = `${process.env.VUE_APP_API}${modulePath}`;
      return axios.get(path, { params });
    },
    getDataService(id, modulePath) {
      this.loading = true;
      this.getServiceById(id, modulePath)
        .then((res) => {
          this.data = res;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async getZipCodeMapping(searchString) {
      const path = `${process.env.VUE_APP_API}/basic/zip-code/?zip_city=${searchString}`;
      const response = await axios.get(path);
      return response.data;
    },
    async getResponsibles(searchString) {
      const path = `${process.env.VUE_APP_API}/auth/responsables/?search=${searchString}`;
      const response = await axios.get(path);
      return response.data;
    },
    async callSingleZipCode(id) {
      const path = `${process.env.VUE_APP_API}/basic/zip-code/?id=${id}`;
      const response = await axios.get(path);
      return response.data;
    },
    async callSingleResponsible(email) {
      const path = `${process.env.VUE_APP_API}/auth/responsables/?search=${email}`;
      const response = await axios.get(path);
      return response.data;
    },
  },
};
