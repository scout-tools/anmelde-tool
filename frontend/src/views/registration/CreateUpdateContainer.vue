<template>
  <v-container fluid class="mt-10">
    <v-card v-if="!isLoading" class="mx-auto top-margin default-max-width">
      <v-row justify="center">
        <v-stepper v-model="currentStep" vertical>
          <template v-for="(step, index) in currentModules">
            <v-stepper-step
              :key="`stepper-${index}`"
              :complete="currentStep > index + 1"
              :step="index + 1"
            >
              {{ `${step.module.header}` }}
            </v-stepper-step>

            <v-divider :key="index"></v-divider>

            <v-stepper-items :key="`stepper-items-${index}`">
              <v-stepper-content :step="index + 1">
                <component
                  :is="step.module.name"
                  :ref="step.module.name"
                  :position="index + 1"
                  :max-pos="currentModules.length"
                  :currentRegistration="currentRegistration"
                  :currentEvent="currentEvent"
                  :personalData="personalData"
                  :currentModule="step"
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
      <LoadingCircual />
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

import LoadingCircual from '@/components/loading/Circual.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import Confirm from './modules/Confirm.vue';
import Food from './modules/Food.vue';
import Introduction from './modules/Introduction.vue';
import Letter from './modules/Letter.vue';
import ParticipantsPersonal from './modules/ParticipantsPersonal.vue';
import Summary from './modules/Summary.vue';
import Tent from './modules/Tent.vue';

export default {
  components: {
    LoadingCircual,
    Confirm,
    Food,
    Introduction,
    Letter,
    ParticipantsPersonal,
    Summary,
    Tent,
  },
  props: ['scoutOrganisation'],
  mixins: [apiCallsMixin],
  data() {
    return {
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      currentEvent: {},
      currentRegistration: {},
      currentModules: [],
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
      const nextStepName = this.currentModules[step].module.name;
      if (
        this.$refs[nextStepName]
        && this.$refs[nextStepName].length
        && this.$refs[nextStepName][0].beforeTabShow
      ) {
        this.$refs[nextStepName][0].beforeTabShow();
      }
    },
    onRegistrationConfirmed() {
      this.callConfirmRegistration();
      this.$router.push({ name: 'eventOverview' });
    },
    callConfirmRegistration() {
      return axios.patch(
        `${process.env.VUE_APP_API}basic/registration/${this.id}/`,
        {
          is_confirmed: true,
        },
      );
    },
    unConfirmRegistration() {
      return axios.patch(
        `${process.env.VUE_APP_API}basic/registration/${this.id}/`,
        {
          is_confirmed: false,
        },
      );
    },
    getData() {
      const registrationId = this.$route.params.id;
      this.isLoading = true;
      this.getRegistration(registrationId).then((response) => {
        this.currentRegistration = response;
        const eventId = this.currentRegistration.event;
        Promise.all([
          this.getEvent(eventId),
          this.getAssignedEventModules(eventId),
          this.getPersonalData(),
        ])
          .then((values) => {
            this.currentEvent = values[0]; // eslint-disable-line
            this.currentModules = values[1].data // eslint-disable-line
            this.personalData = values[2].data // eslint-disable-line

            this.isLoading = false;
          })
          .catch((error) => {
            this.errormsg = error.response.data.message;
            this.isLoading = false;
          });
      });
    },

    async getEvent(id) {
      const path = `${process.env.VUE_APP_API}/event/event/${parseInt(id, 10)}/`;
      const response = await axios.get(path);
      return response.data;
    },

    async getRegistration(id) {
      const path = `${process.env.VUE_APP_API}/event/registration/${id}/`;
      const response = await axios.get(path);
      return response.data;
    },
    loadData() {
      this.getData();
    },
  },
  created() {
    this.loadData();
  },
};
</script>
