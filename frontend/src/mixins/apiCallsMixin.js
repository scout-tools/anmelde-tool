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
    async getService(route) {
      const path = `${process.env.VUE_APP_API}/${route}/`;
      return axios.get(path);
    },
    async getRegService(route, registration) {
      const path = `${process.env.VUE_APP_API}/event/registration/${registration}/${route}/`;
      return axios.get(path);
    },
    async patchRegService(route, regId, field, value) {
      const path = `${process.env.VUE_APP_API}/event/registration/${regId}/${route}/${regId}/`;
      return axios.patch(path, { [field]: value });
    },
    async getRegServiceById(route, registration, id) {
      const path = `${process.env.VUE_APP_API}/event/registration/${registration}/${route}/${id}/`;
      return axios.get(path);
    },
    async getServiceById(route, id) {
      const path = `${process.env.VUE_APP_API}/${route}/${id}/`;
      return axios.get(path);
    },
    patchService(field, value, modulePath, id) {
      const path = `${process.env.VUE_APP_API}${modulePath}${id}/`;
      return axios.patch(path, { [field]: value });
    },
    async updateRegServiceById(route, registration, data) {
      const path = `${process.env.VUE_APP_API}/event/registration/${registration}/${route}/${data.id}/`;
      return axios.put(path, data);
    },
    async deleteRegistration(registration) {
      const path = `${process.env.VUE_APP_API}/event/registration/${registration}/`;
      return axios.delete(path);
    },
    async updateServiceById(route, data) {
      const path = `${process.env.VUE_APP_API}/${route}/${data.id}/`;
      return axios.put(path, data);
    },
    async createServiceById(route, data) {
      const path = `${process.env.VUE_APP_API}/${route}/`;
      return axios.post(path, data);
    },
    async getEventPlanerOverview() {
      const path = `${process.env.VUE_APP_API}/event/event-planer-overview/`;
      return axios.get(path);
    },
    async getEventStatisticsOverview() {
      const path = `${process.env.VUE_APP_API}/event/event-statistics-overview/`;
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
    async getEventOverviewById(id) {
      const path = `${process.env.VUE_APP_API}/event/event-overview/${id}/`;
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
    async addEventModule(data, eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/event-module-mapper/`;
      return axios.post(url, data);
    },
    async deleteEventModule(mapperId, eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/event-module-mapper/${mapperId}/`;
      return axios.delete(url);
    },
    async updateEventModule(data, id, eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/event-module-mapper/${id}/`;
      return axios.put(url, data);
    },
    async getModule(mapperId, eventId) {
      const url = `${this.API_URL}/event/event/${eventId}/event-module-mapper/${mapperId}/attribute-mapper/`;
      return axios.get(url);
    },
    async getPersonalData() {
      const url = `${this.API_URL}/auth/personal-data/`;
      return axios.get(url);
    },
    async getEventSummary(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/`;
      return axios.get(path, { params });
    },
    async getEventLocationSummary(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/locations/`;
      return axios.get(path, { params });
    },
    async getEventKPI(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/kpi/`;
      return axios.get(path);
    },
    async getEventAgeGroups(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/age-groups/`;
      return axios.get(path, { params });
    },
    async getCashSummary(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/cash/`;
      return axios.get(path);
    },
    async addFileRequest(eventId, data) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/files/generate/`;
      return axios.post(path, data);
    },
    async getDownloadSummary(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/files/generate/`;
      return axios.get(path, { params });
    },
    async getAvailableFileTemplates() {
      const path = `${process.env.VUE_APP_API}/event/files/available-templates/`;
      return axios.get(path);
    },
    async getFoodSummary(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/food/`;
      return axios.get(path, { params });
    },
    async getBookingOptions(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/booking-options/`;
      return axios.get(path);
    },
    async getRegistrationSummaryDetails(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/detailed/`;
      return axios.get(path, { params });
    },
    async getParticipants(eventId) {
      const path = `${process.env.VUE_APP_API}/basic/event/${eventId}/participants/`;
      return axios.get(path);
    },
    async getWorkshopSummary(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/workshop/`;
      return axios.get(path);
    },
    async updateMessageById(data) {
      const path = `${process.env.VUE_APP_API}/basic/message/${data.id}/`;
      return axios.put(path, data);
    },
    async getResponsiblePersons(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/emails/responsible-persons/`;
      return axios.get(path, { params });
    },
    async getRegistrationsResponsiblePersons(eventId, params) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/emails/registration-responsible-persons/`;
      return axios.get(path, { params });
    },
  },
};
