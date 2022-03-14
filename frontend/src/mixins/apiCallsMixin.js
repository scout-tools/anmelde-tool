import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
  }),
  methods: {
    async getEvent(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/`;
      return axios.get(path);
    },
    async getEventPlanerOverview() {
      const path = `${process.env.VUE_APP_API}/event/event-planer-overview/`;
      return axios.get(path);
    },
    async getEventForRegistration(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event-registration/${eventId}/`;
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
    async getEventBookingOptions(eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/booking-options/?&timestamp=${new Date().getTime()}`;
      return axios.get(url);
    },
    async addEventBookingOption(eventId, data) {
      const url = `${this.API_URL}/event/event/${eventId}/booking-options/`;
      return axios.post(url, data);
    },
    async updateEventBookingOption(eventId, bookingOptionId, data) {
      const url = `${this.API_URL}/event/event/${eventId}/booking-options/${bookingOptionId}/`;
      return axios.put(url, data);
    },
    async deleteEventBookingOption(eventId, bookingOptionId) {
      const url = `${this.API_URL}/event/event/${eventId}/booking-options/${bookingOptionId}/`;
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
    async getModule(mapperId) {
      const url = `${this.API_URL}/event/event-module-mapper/${mapperId}/attribute-mapper/`;
      return axios.get(url);
    },
    async getPersonalData() {
      const url = `${this.API_URL}/auth/personal-data/`;
      return axios.get(url);
    },
  },
};
