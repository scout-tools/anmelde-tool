<template>
  <v-container fluid>
    <v-card v-if="!isLoading" class="mx-auto top-margin default-max-width">
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
      <LoadingCircual/>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

import LoadingCircual from '@/components/loading/Circual.vue';

import StepConfirm from './steps/00-Common/StepConfirm.vue';
import StepConsent from './steps/00-Common/StepConsent.vue';
import StepConsentSwitch from './steps/00-Common/StepConsentSwitch.vue';
import StepFood from './steps/00-Common/StepFood.vue';
import StepFreeText from './steps/00-Common/StepFreeText.vue';
import AddContract from './steps/00-Common/AddContract.vue';
import StepTents from './steps/00-Common/StepTents.vue';
import StepArrivalMethod from './steps/00-Common/StepArrivalMethod.vue';
import StepArrivalTime from './steps/00-Common/StepArrivalTime.vue';

import StepAddParticipantsSingle from './steps/01-MosaikBundesfahrt21/StepAddParticipantsSingle.vue';
import StepTravelBundesfahrt from './steps/01-MosaikBundesfahrt21/StepTravelBundesfahrt.vue';

import StepAddParticipants from './steps/02-DpvStadtUndSpiel21/StepAddParticipants.vue';
import StepAddParticipantGroupRole from './steps/02-DpvStadtUndSpiel21/StepBdPDpvAddParticipantGroupRole.vue';
import StepBdpDpvLocation from './steps/02-DpvStadtUndSpiel21/StepBdpDpvLocation.vue';
import StepBdpDpvLocationSuggestion from './steps/02-DpvStadtUndSpiel21/StepBdpDpvLocationSuggestion.vue';
import StepBdpDpvPackage from './steps/02-DpvStadtUndSpiel21/StepBdpDpvPackage.vue';
import StepBdpDpVPreferences from './steps/02-DpvStadtUndSpiel21/StepBdpDpVPreferences.vue';
import StepBdpDpvTextForStamm from './steps/02-DpvStadtUndSpiel21/StepBdpDpvTextForStamm.vue';
import StepConfirmDpv from './steps/02-DpvStadtUndSpiel21/StepConfirmDpv.vue';

import StepWorkshop from './steps/03-BusiFe21/StepWorkshop.vue';
import StepConfirmBusife from './steps/03-BusiFe21/StepConfirmBusife.vue';

import DpvGoldErlebnisangebot from './steps/04-DpvGoldErlebnisangebot21/StepErlegbnisAngebot.vue';

// Bundesfahrt 2022 (id=8)
import StepLunchPacket from './steps/08-MosaikBundesfahrt22/StepLunchPacket.vue';
import StepShirt from './steps/08-MosaikBundesfahrt22/StepShirt.vue';
import StepAddParticipantsSingleBundesfahrt from './steps/08-MosaikBundesfahrt22/StepAddParticipantsSingle.vue';

export default {
  components: {
    StepAddParticipantsSingle,
    StepAddParticipants,
    StepFood,
    StepConfirmBusife,
    StepConfirmDpv,
    StepConfirm,
    StepConsent,
    StepBdpDpvLocation,
    StepBdpDpVPreferences,
    StepBdpDpvTextForStamm,
    StepFreeText,
    StepBdpDpvLocationSuggestion,
    StepTravelBundesfahrt,
    StepBdpDpvPackage,
    StepWorkshop,
    LoadingCircual,
    DpvGoldErlebnisangebot,
    AddContract,
    StepTents,
    StepArrivalMethod,
    StepArrivalTime,
    StepAddParticipantsSingleBundesfahrt,
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
      // DPV-Gold
      if (
        this.currentEvent && // eslint-disable-line
        this.currentEvent.eventTags && // eslint-disable-line
        this.currentEvent.eventTags.includes(1)
      ) {
        return [
          StepConsentSwitch,
          StepAddParticipantsSingle,
          StepTents,
          StepArrivalMethod,
          StepArrivalTime,
          StepFreeText,
          StepConfirmBusife,
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
      // DPV-Gold-Erlebnisangebot
      if (
        this.currentEvent && // eslint-disable-line
        this.currentEvent.eventTags && // eslint-disable-line
        this.currentEvent.eventTags.includes(4)
      ) {
        return [
          StepConsent,
          DpvGoldErlebnisangebot,
          AddContract,
          StepFreeText,
          StepConfirm,
        ];
      }
      // Bundesfahrt 22
      if (
        this.currentEvent && // eslint-disable-line
        this.currentEvent.eventTags && // eslint-disable-line
        this.currentEvent.eventTags.includes(8)
      ) {
        return [
          StepConsent,
          StepAddParticipantsSingleBundesfahrt,
          StepArrivalMethod,
          StepShirt,
          StepLunchPacket,
          StepFreeText,
          StepConfirm,
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
