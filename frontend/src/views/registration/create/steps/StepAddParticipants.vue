<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-divider class="text-left my-2" />
      <v-row class="mb-6">
        <span class="subtitle-1"> Gebe die Anzahl der Teilnehmenden an. </span>
      </v-row>
      <v-row class="mb-6">
        <p>
          Du kannst dies Antahl der Teilnehmenden bis zum 1. Mai 2021 anpassen.
          <br />
          Dafür kannst du dich dafür jederzeit wieder einloggen.
        </p>
      </v-row>
      <template v-for="(item, index) in getActiveAgeGroups">
        <v-row :key="`agegroup-${index}`">
          <v-text-field
            v-model="data[item.id]"
            :label="`Anzahl: ${item.description}`"
            required
          >
          </v-text-field>
        </v-row>
      </template>
      <v-divider class="my-3" />
      <v-row class="mb-6">
        <span class="subtitle-1"
          >Du hast Ingesamt {{ total }} Teilnehmer_innen angemeldet</span
        >
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
// import axios from 'axios';
import { mapGetters } from 'vuex';
// import { required, minLength, minValue } from 'vuelidate/lib/validators';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Teilnehmende',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {},
  }),
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'ageGroupMapping',
    ]),
    total() {
      return Object.values(this.data).reduce(
        (pv, cv) => parseInt(pv, 10) + parseInt(cv, 10),
        0,
      );
    },
    getActiveAgeGroups() {
      if (
        this.ageGroupMapping && // eslint-disable-line
        this.currentEvent && // eslint-disable-line
        this.currentEvent.ageGroups && // eslint-disable-line
        this.currentEvent.ageGroups.length
      ) {
        return this.ageGroupMapping.filter((item) =>
          this.currentEvent.ageGroups.includes(item.id), // eslint-disable-line
        );  // eslint-disable-line
      }
      return [];
    },
  },
  methods: {
    greaterThanZero(value) {
      return value > 0;
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.valid) {
        return;
      }

      this.$emit('nextStep');
    },
    addParticipants() {
      // const promises = [];
      // const registrationId = this.$route.params.id;
      // const myUrl = `${this.API_URL}basic/participant-group/`;
      // const valueArray = Object.values(this.data);
      // Object.keys(this.data).forEach((element, index) => {
      //   const paramsData = {
      //     ageGroup: parseInt(element, 10),
      //     numberOfPersons: parseInt(valueArray[index], 10),
      //     registration: parseInt(registrationId, 10),
      //   };
      //   promises.push(axios.post(myUrl, paramsData));
      // });
      // Promise.all(promises).then(() => {
      //   this.$emit('nextStep');
      // });
    },
    beforeTabShow() {},
  },
};
</script>
