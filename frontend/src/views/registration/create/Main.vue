<template>
  <v-card class="mx-auto top-margin">
    <v-row justify="center">
      <v-stepper v-model="currentStep" vertical>
        <template v-for="(step, index) in steps">
          <v-stepper-step
            :key="`stepper-${index}`"
            :complete="currentStep > index + 1"
            :step="index + 1"
          >
            {{ `${index + 1} Schritt`  }}
          </v-stepper-step>

          <v-divider :key="index"></v-divider>

          <v-stepper-items :key="`stepper-items-${index}`">
            <v-stepper-content :step="index + 1">
              <component
                :is="step"
                :ref="step.name"
                :position="index + 1"
                :max-pos="steps.length"
                :currentRegistration="currentRegistration"
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

import StepAddParticipantsSingle from './steps/StepAddParticipantsSingle.vue';
import StepAddParticipants from './steps/StepAddParticipants.vue';
import StepConfirm from './steps/StepConfirm.vue';
import StepConsent from './steps/StepConsent.vue';
import StepFood from './steps/StepFood.vue';
import StepBdpDpvLocation from './steps/StepBdpDpvLocation.vue';
import StepBdpDpVPreferences from './steps/StepBdpDpVPreferences.vue';

export default {
  components: {
    StepAddParticipantsSingle,
    StepAddParticipants,
    StepFood,
    StepConfirm,
    StepConsent,
    StepBdpDpvLocation,
    StepBdpDpVPreferences,
  },
  data() {
    return {
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      currentEvent: [],
      currentRegistration: [],
      data: {
        event: {
          responsiblePersons: ['robert@hratuga.de'],
        },
      },
    };
  },
  computed: {
    steps() {
      // Bundesfahrt
      if (this.currentEvent
        && this.currentEvent.eventTags
        && this.currentEvent.eventTags.includes(1)) {
        return [
          StepConsent,
          StepAddParticipantsSingle,
          StepConfirm,
        ];
      }
      // BdP-DPV
      if (this.currentEvent
        && this.currentEvent.eventTags
        && this.currentEvent.eventTags.includes(2)) {
        return [
          StepConsent,
          StepAddParticipants,
          StepBdpDpvLocation,
          StepBdpDpVPreferences,
          StepConfirm,
        ];
      }
      return [
        StepConsent,
        StepAddParticipants,
        StepFood,
        StepConfirm,
      ];
    },
    headerSteps() {
      return ['Teilnehmer', 'Essen', 'Bestätigung'];
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
      this.$router.push({ name: 'eventOverview' });
    },
    callConfirmRegistration() {
      return axios.post(`${process.env.VUE_APP_API}basic/event/`, {
        responsiblePersons: ['robert@hratuga.de'],
        event: 1,
        scoutOrganisation: 39,
      });
    },
    getEvent(id) {
      const path = `${process.env.VUE_APP_API}basic/event/${parseInt(id, 10)}/`;
      axios
        .get(path)
        .then((res) => {
          this.currentEvent = res.data;
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getRegistration() {
      const path = `${process.env.VUE_APP_API}basic/registration/${this.$route.params.id}/`;
      axios
        .get(path)
        .then((res) => {
          this.currentRegistration = res.data;
          this.getEvent(res.data.event);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    loadData() {
      if (!this.$route.params.event) {
        this.getRegistration();
      } else {
        this.getEvent(this.$route.params.event);
      }
    },
  },
  created() {
    this.loadData();
  },

};
</script>
