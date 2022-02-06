export default {
  namespaced: true,
  state: () => ({
    event: {
      description: '',
      endTime: '',
      id: '',
      lastPossibleUpdate: '',
      location: '',
      name: '',
      price: '',
      registrationDeadline: '',
      registrationModel: '',
      registrationStart: '',
      startTime: '',
      tags: [],
      eventmodulemapperSet: [],
      responsiblePersons: [],
      keycloakPath: null,
      keycloakAdminPath: null,
    },
  }),
  mutations: {
    setEvent(state, event) {
      state.event = event;
    },
    setEventName(state, name) {
      state.event.name = name;
    },
    setEventDescription(state, description) {
      state.event.description = description;
    },
    setEventAttribute(state, {
      prop,
      value,
    }) {
      state.event[prop] = value;
    },
    addEventTags(state, tags) {
      state.event.tags = [...state.event.tags, ...tags];
    },
    setEventTags(state, tags) {
      state.event.tags = tags;
    },
    setKeycloakGroup(state, group) {
      state.event.keycloakPath = group;
    },
    setKeycloakAdminGroup(state, group) {
      state.event.keycloakAdminPath = group;
    },
    setResponsiblePersons(state, persons) {
      state.event.responsiblePersons = persons;
    },
    setRegistrationModel(state, model) {
      state.event.registrationModel = model;
    },
  },
  actions: {},
  getters: {
    event(state) {
      return state.event;
    },
  },
};
