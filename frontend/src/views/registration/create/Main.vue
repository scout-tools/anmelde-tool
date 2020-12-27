<template>
  <v-card max-width="600" class="mx-auto">
    <v-row justify="center">
      <v-stepper v-model="currentStep" vertical>
        <template v-for="(step, index) in steps">
          <v-stepper-step
            :key="`stepper-${index}`"
            :complete="currentStep > index + 1"
            :step="index + 1"
          >
            {{ headerSteps[index] }}
          </v-stepper-step>

          <v-divider :key="index"></v-divider>

          <v-stepper-items :key="`stepper-items-${index}`">
            <v-stepper-content :step="index + 1">
              <component
                :is="step"
                :ref="step.name"
                :position="index + 1"
                :max-pos="steps.length"
                :currentEvent="currentEvent"
                @prevStep="prevStep()"
                @nextStep="nextStep()"
                @submit="onRegistrationConfirmed()"
              />
            </v-stepper-content>
          </v-stepper-items>
        </template>
      </v-stepper>
    </v-row>
    <v-snackbar v-model="showSuccess" color="success" y="top" :timeout="timeout">
      {{ 'Die Aktion wurde erfolgreich angelegt.' }}
    </v-snackbar>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
      {{ 'Fehler beim Speichern der Aktion' }}
    </v-snackbar>
  </v-card>
</template>

<script>
import axios from 'axios';

import StepAddParticipants from './steps/StepAddParticipants.vue';
import StepConsent from './steps/StepConsent.vue';
import StepConfirm from './steps/StepConfirm.vue';

export default {
  components: {
    StepConsent,
    StepAddParticipants,
    StepConfirm,
  },
  data() {
    return {
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      currentEvent: [],
      data: {
        event: {},
      },
    };
  },
  computed: {
    steps() {
      return [
        StepConsent,
        StepAddParticipants,
        StepConfirm,
      ];
    },
    headerSteps() {
      return ['Einwilligung', 'Teilnehmer', 'Bestätigung'];
    },
  },
  methods: {
    nextStep() {
      this.currentStep += 1;
    },
    prevStep() {
      this.currentStep -= 1;
    },
    onRegistrationConfirmed() {
      // onRegistrationConfirmed
    },
    callConfirmRegistration() {
      return axios.post(`${process.env.VUE_APP_API}basic/event/`, this.data.event);
    },
    getEvent() {
      const path = `${process.env.VUE_APP_API}basic/event/${this.$route.params.event}/`;
      axios
        .get(path)
        .then((res) => {
          this.currentEvent = res.data;
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getEvent();
  },
};
</script>
