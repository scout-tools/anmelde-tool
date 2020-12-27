<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-divider class="text-left my-2" />
      <v-row class="mb-6">
        <span class="subtitle-1"> Gebe die Anzahl der Teilnehmer an.</span>
      </v-row>
      <template v-for="(item, index) in getActiveAgeGroups">
        <v-row :key="`agegroup-${index}`">
          <v-text-field v-model="data[item.id]" :label="`Anzahl ${item.name}`" required>
          </v-text-field>
        </v-row>
      </template>
      <v-divider class="my-3" />
      <v-row class="mb-6">
        <span class="subtitle-1">Du hast Ingesamt {{ total }} Teilnehmer angemeldet</span>
      </v-row>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
    },
  }),
  validations: {},
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchy', 'ageGroupMapping']),
    total() {
      return Object.values(this.data).reduce((pv, cv) => parseInt(pv, 10) + parseInt(cv, 10), 0);
    },
    getActiveAgeGroups() {
      if (
        this.ageGroupMapping
        && this.currentEvent
        && this.currentEvent.ageGroups
        && this.currentEvent.ageGroups.length
      ) {
        return this.ageGroupMapping.filter((item) => this.currentEvent.ageGroups.includes(item.id));
      }
      return [];
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }

      this.addParticipants();
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    addParticipants() {
      const promises = [];
      const registrationId = this.$route.params.id;
      const myUrl = `${this.API_URL}basic/participants/`;
      const valueArray = Object.values(this.data);
      Object.keys(this.data).forEach((element, index) => {
        const paramsData = {
          ageGroup: parseInt(element, 10),
          numberOfPersons: parseInt(valueArray[index], 10),
          registration: parseInt(registrationId, 10),
        };
        promises.push(axios.post(myUrl, paramsData));
      });

      Promise.all(promises).then(() => {
        this.$emit('nextStep');
      });
    },
  },
};
</script>
