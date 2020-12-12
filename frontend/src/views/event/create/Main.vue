<template>
  <v-container>
    <v-row justify="center">
      <v-flex
        ma-3
        lg9
      >
        <v-stepper
          alt-labels
          vertical
          v-model="currentStep"
        >
          <v-stepper-header>
            <template v-for="index in steps.length">
              <v-stepper-step
                :key="`${index}-step`"
                :complete="currentStep > index"
                :step="index"
              >
                {{ headerStep[index-1] }}
              </v-stepper-step>

              <v-divider
                v-if="index !== index"
                :key="index"
              ></v-divider>
            </template>
          </v-stepper-header>

          <v-stepper-items v-for="(step, index) in steps" :key="index">
            <v-stepper-content
              :step="index+1"
            >
              <component
                :is="step"
                :ref="step.name"
                :data="data"
                :position="index+1"
                :max-pos="steps.length"
                @prevStep="prevStep()"
                @nextStep="nextStep()"
                @submit="finish()"
              />
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-flex>
    </v-row>
    <v-snackbar
      v-model="showError"
      color="error"
      y='top'
      :timeout="timeout"
    >
      {{ 'Fehler beim Speichern der Aktion' }}
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios';

import StepNameDescription from './steps/StepNameDescription.vue';
import StepLocation from './steps/StepLocation.vue';
import StepAgeGroup from './steps/StepAgeGroup.vue';
import StepEventContact from './steps/StepEventContact.vue';
import StepStartEndDeadline from './steps/StepStartEndDeadline.vue';

export default {
  components: {
    StepNameDescription,
    StepLocation,
    StepAgeGroup,
    StepEventContact,
    StepStartEndDeadline,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      currentStep: 1,
      steps: [StepNameDescription, StepStartEndDeadline, StepLocation, StepAgeGroup, StepEventContact], // eslint-disable-line max-len
      showError: false,
      showSuccess: false,
      timeout: 7000,
      headerStep: [
        'Beschreibung',
        'Daten und Uhrzeit',
        'Ort',
        'Zielgruppe',
        'Kontaktdaten',
      ],
      data: [],
    };
  },

  methods: {
    nextStep() {
      this.currentStep += 1;
    },
    prevStep() {
      this.currentStep -= 1;
    },
    async finish() {
      const dataNameDescription = this.$refs.StepNameDescription[0].getData();
      const dataStartEndDeadline = this.$refs.StepStartEndDeadline[0].getData();
      const dataStepLocation = this.$refs.StepLocation[0].getData();
      const dataStepAgeGroup = this.$refs.StepAgeGroup[0].getData();
      const dataStepEventContact = this.$refs.StepEventContact[0].getData();

      const data = {
        name: dataNameDescription.name,
        description: dataNameDescription.description,
        location: dataStepLocation.location_id,
        ageGroups: dataStepAgeGroup.ageGroups,
        contact: dataStepEventContact.contact_id,
        startTime: dataStartEndDeadline.startTime,
        endTime: dataStartEndDeadline.endTime,
        registrationDeadline: dataStartEndDeadline.deadline,
      };

      const result = await axios.post(`${this.API_URL}basic/event/`, data);
      console.log(result);
    },
  },
};
</script>
