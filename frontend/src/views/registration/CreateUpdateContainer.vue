<template>
  <v-container fluid class="mt-10 default-width top-margin">
    <v-card flat v-if="!loading" class="mx-auto top-margin default-width">
      <v-row justify="center" style="width: 100%">
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
              <v-stepper-content :step="index + 1" class="default-width" style="width: 100%">
                <component
                  :is="step.module.name"
                  :ref="step.module.name"
                  :position="index + 1"
                  :max-pos="currentModules.length"
                  :currentRegistration="currentRegistration"
                  :currentEvent="currentEvent"
                  :personalData="personalData"
                  :currentModule="step"
                  @ignore="nextStep()"
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

import Food from './modules/Food.vue';
import Introduction from './modules/Introduction.vue';
import Letter from './modules/Letter.vue';
import ParticipantsPersonal from './modules/ParticipantsPersonal.vue';
import Summary from './modules/Summary.vue';
import Tent from './modules/Tent.vue';
import Travel from './modules/Travel.vue';
import TravelBack from './modules/TravelBack.vue';
import LunchMeals from './modules/LunchMeals.vue';
import Tshirts from './modules/Tshirts.vue';
import SubscribeWorkshop from './modules/SubscribeWorkshop.vue';

import ParticipantsPersonalGold from './modules/ParticipantsPersonalGold.vue';
import ParticipantsPersonalSmall from './modules/ParticipantsPersonalSmall.vue';
import TravelBundesfahrt from './modules/TravelBundesfahrt.vue';

export default {
  components: {
    LoadingCircual,
    Food,
    Introduction,
    Letter,
    ParticipantsPersonal,
    ParticipantsPersonalGold,
    Summary,
    Tent,
    Travel,
    TravelBack,
    SubscribeWorkshop,
    LunchMeals,
    Tshirts,
    TravelBundesfahrt,
    ParticipantsPersonalSmall,
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
      loading: true,
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
        this.$refs[nextStepName] && // eslint-disable-line
        this.$refs[nextStepName].length && // eslint-disable-line
        this.$refs[nextStepName][0].beforeTabShow
      ) {
        this.$refs[nextStepName][0].beforeTabShow();
      }
    },
    onRegistrationConfirmed() {
      this.callConfirmRegistration().then(() => {
        this.$router.push({
          name: 'registrationCompleted',
          params: { id: this.currentRegistration.id },
        });
      });
    },
    callConfirmRegistration() {
      return axios.put(
        `${process.env.VUE_APP_API}/event/registration/${this.currentRegistration.id}/`,
        {
          is_confirmed: true,
        },
      );
    },
    getData() {
      const registrationId = this.$route.params.id;
      this.loading = true;
      this.getRegistration(registrationId)
        .then((response) => {
          this.currentRegistration = response;
          const eventId = this.currentRegistration.event;
          Promise.all([
            this.getEventForRegistration(eventId),
            this.getAssignedEventModules(eventId),
            this.getPersonalData(),
          ])
            .then((values) => {
              this.currentEvent = values[0].data; // eslint-disable-line
              this.currentModules = values[1].data; // eslint-disable-line
              this.personalData = values[2].data; // eslint-disable-line

              this.loading = false;
            })
            .catch((error) => {
              this.errormsg = error.response.data.message;
              this.loading = false;
            });
        })
        .catch((error) => {
          console.log(error.response);
          this.$router.push({ name: 'eventOverview' });
        });
    },

    async getEvent(id) {
      const path = `${process.env.VUE_APP_API}/event/event/${parseInt(
        id,
        10,
      )}/`;
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
