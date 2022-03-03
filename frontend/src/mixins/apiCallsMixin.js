import axios from 'axios';

export default {
  methods: {
    async getEvent(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.get(path);
    },
    async getEventPlanerOverview() {
      const path = `${process.env.VUE_APP_API}/event/event-planer-overview/`;
      return axios.get(path);
    },
    async getEventOverview() {
      const path = `${process.env.VUE_APP_API}/event/event-overview/`;
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
    async getEventSleepingLocation(eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/sleeping-locations/?&timestamp=${new Date().getTime()}`;
      return axios.get(url);
    },
    async addEventSleepingLocation(eventId, data) {
      const url = `${this.API_URL}/event/event/${eventId}/sleeping-locations/`;
      return axios.post(url, data);
    },
    async updateEventSleepingLocation(eventId, sleepingLocationId, data) {
      const url = `${this.API_URL}/event/event/${eventId}/sleeping-locations/${sleepingLocationId}/`;
      return axios.put(url, data);
    },
    async deleteEventSleepingLocation(eventId, sleepingLocationId) {
      const url = `${this.API_URL}/event/event/${eventId}/sleeping-locations/${sleepingLocationId}/`;
      return axios.delete(url);
    },
    async getAvailableEventModules(eventId) {
      const urlAvailableModules = `${this.API_URL}/event/event/${eventId}/available-modules/`;
      return axios.get(urlAvailableModules);
    },
    async getAssignedEventModules(eventId) {
      const urlAssignedModules = `${this.API_URL}/event/event/${eventId}/assigned-event-modules/`;
      return axios.get(urlAssignedModules);
    },
    async addEventModule(data) {
      const url = `${this.API_URL}/event/event-module-mapper/`;
      return axios.post(url, data);
    },
    async deleteEventModule(mapperId) {
      const url = `${this.API_URL}/event/event-module-mapper/${mapperId}/`;
      return axios.delete(url);
    },
  },
};
