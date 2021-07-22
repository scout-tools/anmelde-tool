import axios from 'axios';

export const serviceMixin = {  // eslint-disable-line
  methods: {
    async postExperimentItem(event, experiment, score) {
      const path = `${process.env.VUE_APP_API}basic/experiment-item/`;
      return axios.post(path, {
        event,
        experiment,
        score,
      });
    },
    async getRegistrationStats(eventId) {
      const path = `${process.env.VUE_APP_API}basic/event/${eventId}/registration-stats/`;
      return axios.get(path);
    },
    async getWorkshopStats() {
      const path = `${process.env.VUE_APP_API}basic/workshop-stats/`;
      return axios.get(path);
    },
  },
};
