import axios from 'axios';

export default {
  methods: {
    async getRegistrationStats(eventId) {
      const path = `${process.env.VUE_APP_API}basic/event/${eventId}/registration-stats/`;
      return axios.get(path);
    },
    async getParticipants(eventId) {
      const path = `${process.env.VUE_APP_API}basic/event/${eventId}/participants/`;
      return axios.get(path);
    },
    async getWorkshopStats(eventId) {
      const path = `${process.env.VUE_APP_API}basic/event/${eventId}/workshop-eventmaster-overview/`;
      return axios.get(path);
    },
    async getEvent(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.get(path);
    },
    async updateEvent(eventId, data) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.put(path, data);
    },
  },
};
