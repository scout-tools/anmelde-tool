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
  },
  actions: {},
  getters: {
    event(state) {
      return state.event;
    },
  },
};
