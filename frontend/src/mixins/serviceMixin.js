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
      const path = `${process.env.VUE_APP_API}/basic/event/${eventId}/registration-stats/`;
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
  },
};
