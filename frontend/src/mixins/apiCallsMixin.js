import axios from 'axios';

export default {
  methods: {
    async getEvent(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.get(path);
    },
    async updateEvent(eventId, data) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.put(path, data);
    },
    async getTag(type) {
      const path = `${this.API_URL}/basic/tags/?type__name=${type}`;
      return axios.get(path);
    },
    async searchZipCode(searchKeyword) {
      const path = `${this.API_URL}/basic/zip-code/?zip_city=${searchKeyword}`;
      const response = await axios.get(path);
      return response.data;
    },
    async getEventLocation() {
      const url = `${this.API_URL}/event/event-location/?&timestamp=${new Date().getTime()}`;
      return axios.get(url);
    },
  },
};
