<template>
  <v-container>
    <v-card v-if="!isLoading" class="mx-auto top-margin">
      <v-row justify="center">
        <v-stepper v-model="currentStep" vertical>
          <template v-for="(step, index) in steps">
            <v-stepper-step
              :key="`stepper-${index}`"
              :complete="currentStep > index + 1"
              :step="index + 1"
            >
              {{ `${step.displayName}` }}
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
                  :scoutOrganisation="scoutOrganisation"
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
      <v-snackbar
        v-model="showSuccess"
        color="success"
        y="top"
        :timeout="timeout"
      >
        {{ 'Die Aktion wurde erfolgreich angelegt.' }}
      </v-snackbar>
      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Speichern der Aktion' }}
      </v-snackbar>
    </v-card>
    <v-card v-else>
      <div class="text-center ma-5">
        <p>Lade Daten ...</p>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
        <p>Bitte hab etwas Geduld.</p>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

import StepAddParticipantsSingle from './steps/StepAddParticipantsSingle.vue';
import StepAddParticipants from './steps/StepAddParticipants.vue';
import StepConfirmBundesfahrt from './steps/StepConfirmBundesfahrt.vue';
import StepConfirmDpv from './steps/StepConfirmDpv.vue';
import StepBdpDpvPackage from './steps/StepBdpDpvPackage.vue';
import StepConfirm from './steps/StepConfirm.vue';
import StepConsent from './steps/StepConsent.vue';
import StepFood from './steps/StepFood.vue';
import StepBdpDpvLocation from './steps/StepBdpDpvLocation.vue';
import StepBdpDpVPreferences from './steps/StepBdpDpVPreferences.vue';
import StepTents from './steps/StepTents.vue';
// import StepTravel from './steps/StepTravel.vue';
import StepAddParticipantGroupRole from './steps/StepBdPDpvAddParticipantGroupRole.vue';
import StepBdpDpvTextForStamm from './steps/StepBdpDpvTextForStamm.vue';
// import StepTravelBack from './steps/StepTravelBack.vue';
import StepTravelBundesfahrt from './steps/StepTravelBundesfahrt.vue';
import StepBdpDpvLocationSuggestion from './steps/StepBdpDpvLocationSuggestion.vue';
import StepWorkshop from './steps/StepWorkshop.vue';

export default {
  components: {
    StepAddParticipantsSingle,
    StepAddParticipants,
    StepFood,
    StepConfirmBundesfahrt,
    StepConfirmDpv,
    StepConfirm,
    StepConsent,
    StepBdpDpvLocation,
    StepBdpDpVPreferences,
    StepBdpDpvTextForStamm,
    StepBdpDpvLocationSuggestion,
    StepTravelBundesfahrt,
    StepBdpDpvPackage,
    StepWorkshop,
  },
  props: ['scoutOrganisation'],
  data() {
    return {
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      currentEvent: [],
      currentRegistration: [],
      isLoading: true,
      data: {
        event: {
          responsiblePersons: [''],
        },
      },
    };
  },
  computed: {
    id() {
      return this.$route.params.id;
    },
    steps() {
      // Bundesfahrt
      if (
        this.currentEvent && // eslint-disable-line
        this.currentEvent.eventTags && // eslint-disable-line
        this.currentEvent.eventTags.includes(1)
      ) {
        return [
          StepConsent,
          StepAddParticipantsSingle,
          StepTents,
          StepWorkshop,
          StepConfirmBundesfahrt,
        ];
      }
      // BdP-DPV
      if (
        this.currentEvent && // eslint-disable-line
        this.currentEvent.eventTags && // eslint-disable-line
        this.currentEvent.eventTags.includes(2)
      ) {
        return [
          StepConsent,
          StepAddParticipantGroupRole,
          StepBdpDpvLocation,
          StepBdpDpVPreferences,
          StepBdpDpvTextForStamm,
          StepBdpDpvLocationSuggestion,
          StepBdpDpvPackage,
          StepConfirmDpv,
        ];
      }
      return [StepConsent, StepAddParticipants, StepFood, StepConfirm];
    },
  },
  methods: {
    nextStep() {
      this.currentStep += 1;
      this.callOnBeforeTab(this.currentStep - 1);
    },
    prevStep() {
      this.currentStep -= 1;
      this.callOnBeforeTab(this.currentStep - 1);
    },
    callOnBeforeTab(step) {
      const nextStepName = this.steps[step].name;
      if (this.$refs[nextStepName]
        && this.$refs[nextStepName].length
        && this.$refs[nextStepName][0].beforeTabShow) {
        this.$refs[nextStepName][0].beforeTabShow();
      }
    },
    onRegistrationConfirmed() {
      this.callConfirmRegistration();
      this.$router.push({ name: 'eventOverview' });
    },
    callConfirmRegistration() {
      return axios.patch(`${process.env.VUE_APP_API}basic/registration/${this.id}/`, {
        is_confirmed: true,
      });
    },
    unConfirmRegistration() {
      return axios.patch(`${process.env.VUE_APP_API}basic/registration/${this.id}/`, {
        is_confirmed: false,
      });
    },
    getEvent(id) {
      this.isLoading = true;
      Promise.all([this.getEventData(id)])
        .then((values) => {
          [this.currentEvent] = values;

          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },

    async getEventData(id) {
      const path = `${process.env.VUE_APP_API}basic/event/${parseInt(id, 10)}/`;
      const response = await axios.get(path);

      return response.data;
    },

    getRegistration() {
      const path = `${process.env.VUE_APP_API}basic/registration/${this.$route.params.id}/`;
      axios
        .get(path)
        .then((res) => {
          this.currentRegistration = res.data;
          this.getEvent(res.data.event);
          this.unConfirmRegistration();
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
