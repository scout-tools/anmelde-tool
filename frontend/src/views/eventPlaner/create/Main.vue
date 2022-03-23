<template>
  <v-container>
    <v-card class="mx-auto my-12">
      <v-card-title>
        Aktion bearbeiten
      </v-card-title>
      <v-card-subtitle>
        Viele Pfadfinder_innen und Pfadfinder freuen sich schon auf deine Aktion. {{ maxStepsText }}
        Viel Spaß!
      </v-card-subtitle>
      <v-card-text>
        Manche Abschnitte geben vor, was abgefragt werden soll und manche sind mehr optionaler
        Natur.
        Bei manchen kann man noch zusätzliche Abfragen einbauen.
      </v-card-text>
      <v-stepper v-model="currentStep" vertical class="mt-5">
        <template v-for="(step, index) in steps">
          <v-stepper-step
            :key="`stepper-${index}`"
            :complete="currentStep > index + 1"
            :step="index + 1">
            {{ step.header }}
          </v-stepper-step>

          <v-divider :key="index"/>

          <v-stepper-items :key="`stepper-items-${index}`">
            <v-stepper-content :step="index + 1">
              <component
                :is="step"
                :event="event"
                :ref="step.name"
                :position="index + 1"
                :max-pos="maxSteps"
                @prevStep="prevStep"
                @nextStep="nextStep"
                @submit="onCreateEventClick"
              />
            </v-stepper-content>
          </v-stepper-items>
        </template>
      </v-stepper>
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
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import store from '@/store';
import StepRegistrationOverview
  from '@/views/eventPlaner/create/steps/StepRegistrationOverview.vue';
import StepNameDescription from './steps/StepNameDescription.vue';
import StepLocation from './steps/StepLocation.vue';
import StepEventContact from './steps/StepEventContact.vue';
import StepStartEndDeadline from './steps/StepStartEndDeadline.vue';
import StepParticipationFeeSimple from './steps/StepParticipationFeeSimple.vue';
import StepInvitationCode from './steps/StepInvitationCode.vue';
import StepEventTags from './steps/StepEventTags.vue';
import StepVisibility from './steps/StepVisibility.vue';
import StepMasterData from './steps/StepMasterData.vue';
import StepParticipationFeeComplex from './steps/StepParticipationFeeComplex.vue';
import StepEventAuthenticationInternal from './steps/StepEventAuthenticationInternal.vue';
import StepEventAuthenticationKeycloak from './steps/StepEventAuthenticationKeycloak.vue';
import StepEventRegistrationModel from './steps/StepEventRegistrationModel.vue';

export default {
  name: 'PlanEvent',
  mixins: [apiCallsMixin],
  components: {
    StepNameDescription,
    StepLocation,
    StepEventContact,
    StepStartEndDeadline,
    StepParticipationFeeSimple,
    StepInvitationCode,
    StepEventTags,
    StepVisibility,
    StepMasterData,
    StepParticipationFeeComplex,
    StepEventAuthenticationInternal,
    StepEventAuthenticationKeycloak,
    StepEventRegistrationModel,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      isLoading: true,
      isSingleStep: false,
    };
  },
  computed: {
    steps() {
      let sleepingLocation;
      if (this.event.eventPlanerModules.includes('BookingOptionComplex')) {
        sleepingLocation = StepParticipationFeeComplex;
      } else {
        sleepingLocation = StepParticipationFeeSimple;
      }
      let authorization;
      if (this.event.eventPlanerModules.includes('KeycloakAuthorization')) {
        authorization = StepEventAuthenticationKeycloak;
      } else {
        authorization = StepEventAuthenticationInternal;
      }

      return [
        StepNameDescription,
        StepMasterData,
        StepInvitationCode,
        StepStartEndDeadline,
        StepLocation,
        sleepingLocation,
        authorization,
        StepEventRegistrationModel,
        StepVisibility,
        StepRegistrationOverview,
      ];
    },
    id() {
      return this.$route.params.id;
    },
    maxSteps() {
      return this.isSingleStep ? 1 : this.steps.length;
    },
    maxStepsText() {
      if (this.maxSteps === 1) {
        return 'Bitte bearbeite diesen kleinen Schritt.';
      }
      return `Im folgenden führen wir dich durch ${this.maxSteps} kleine Schritt.`;
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
      if (
        this.$refs[nextStepName]
        && this.$refs[nextStepName].length
        && this.$refs[nextStepName][0].beforeTabShow
      ) {
        this.$refs[nextStepName][0].beforeTabShow();
      }
    },
    onCreateEventClick() {
      this.handleCreateEventRequest();
    },
    async handleCreateEventRequest() {
      this.updateEvent(this.id, this.event)
        .then(() => {
          this.showSuccess = true;
          this.$router.push({ name: 'eventPlaner' });
        })
        .catch((error) => {
          console.log(error);
          this.showError = true;
        });
    },
    getData() {
      this.isLoading = true;
      this.getEvent(this.$route.params.id)
        .then((success) => {
          store.commit('createEvent/setEvent', success.data);
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
          this.$router.push({ name: 'eventPlaner' });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  created() {
    if (!this.$route.params.id) {
      this.$root.globalSnackbar.show({
        message: 'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später noch einmal.',
        color: 'error',
      });
      this.$router.push({ name: 'eventPlaner' });
    }

    this.getData();

    if (this.$route.params.step) {
      this.isSingleStep = true;
      this.currentStep = this.$route.params.step;
    }
    this.callOnBeforeTab(this.currentStep - 1);
  },
};
</script>
