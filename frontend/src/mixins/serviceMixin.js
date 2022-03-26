import axios from 'axios';

export default {
  // eslint-disable-line
  methods: {
    async postExperimentItem(event, experiment, score) {
      const path = `${process.env.VUE_APP_API}basic/experiment-item/`;
      return axios.post(path, {
        event,
        experiment,
        score,
      });
    },
    async getRegistrationSummary(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/`;
      return axios.get(path);
    },
    async getParticipants(eventId) {
      const path = `${process.env.VUE_APP_API}/basic/event/${eventId}/participants/`;
      return axios.get(path);
    },
    async getWorkshopStats(eventId) {
      const path = `${process.env.VUE_APP_API}/basic/event/${eventId}/workshop-eventmaster-overview/`;
      return axios.get(path);
    },
    async getServiceById(id, modulePath) {
      const path = `${process.env.VUE_APP_API}${modulePath}${id}/`;
      const response = await axios.get(path);

      return response.data;
    },
    patchService(field, value, modulePath) {
      const path = `${process.env.VUE_APP_API}${modulePath}${this.id}/`;
      return axios.patch(path, { [field]: value });
    },
    getSimpleService(modulePath) {
      const path = `${process.env.VUE_APP_API}${modulePath}`;
      return axios.get(path);
    },
    getService(id, modulePath) {
      this.isLoading = true;
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
          this.isLoading = false;
        });
    },
    getLookup(lookupPath) {
      this.isLoading = true;
      this.getSimpleService(lookupPath)
        .then((res) => {
          this.lookupList = res.data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    async getZipCodeMapping(searchString) {
      const path = `${process.env.VUE_APP_API}/basic/zip-code/?zip_city=${searchString}`;
      const response = await axios.get(path);
      return response.data;
    },
    async callSingleZipCode(id) {
      const path = `${process.env.VUE_APP_API}/basic/zip-code/?id=${id}`;
      const response = await axios.get(path);
      return response.data;
    },
  },
};
