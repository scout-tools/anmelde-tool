export default {
  namespaced: true,
  state: () => ({
    event: {
      description: '',
      endDate: '',
      id: '',
      lastPossibleUpdate: '',
      location: '',
      name: '',
      price: '',
      registrationDeadline: '',
      singleRegistration: '',
      groupRegistration: '',
      startDate: '',
      tags: [],
      eventmodulemapperSet: [],
      responsiblePersons: [],
      keycloakPath: null,
      keycloakAdminPath: null,
      personalDataRequired: false,
      eventPlanerModules: [],
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
    setRegistrationTypeSingle(state, model) {
      state.event.singleRegistration = model;
    },
    setRegistrationTypeGroup(state, model) {
      state.event.groupRegistration = model;
    },
    setPersonalDateRequired(state, required) {
      state.event.personalDataRequired = required;
    },
  },
  actions: {},
  getters: {
    event(state) {
      return state.event;
    },
  },
};
