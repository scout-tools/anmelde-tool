<template>
  <v-container>
    <v-card v-if="!isLoading" class="mx-auto my-12">
      <v-row justify="center">
        <v-stepper v-model="currentStep" vertical>
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
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import StepNameDescription from './steps/StepNameDescription.vue';
import StepLocation from './steps/StepLocation.vue';
import StepEventContact from './steps/StepEventContact.vue';
import StepStartEndDeadline from './steps/StepStartEndDeadline.vue';
import StepParticipationFee from './steps/StepParticipationFee.vue';
import StepInvitationCode from './steps/StepInvitationCode.vue';
import StepEventTags from './steps/StepEventTags.vue';
import StepVisibility from './steps/StepVisibility.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import store from '@/store';

export default {
  name: 'PlanEvent',
  mixins: [apiCallsMixin],
  components: {
    StepNameDescription,
    StepLocation,
    StepEventContact,
    StepStartEndDeadline,
    StepParticipationFee,
    StepInvitationCode,
    StepEventTags,
    StepVisibility,
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
      modules: {
        Introduction: StepNameDescription,
        VerifyEventCode: StepInvitationCode,
        DatesAndTimes: StepStartEndDeadline,
        EventLocation: StepLocation,
        Tags: StepEventTags,
        SleepingLocationComplex: StepParticipationFee,
        SleepingLocationEasy: StepParticipationFee,
        ContactData: StepEventContact,
        Public: StepVisibility,
        InternalAuthentication: StepEventContact,
        KeycloakAuthentication: StepEventContact,
        OfferWorkshop: StepEventContact,
        SubscribeWorkshop: StepEventContact,
      },
    };
  },
  computed: {
    steps() {
      const stepList = [];
      this.event.eventmodulemapperSet.forEach((item) => {
        stepList.push(this.modules[item.module.name]);
      });

      return stepList;
      // return [
      //   StepNameDescription,
      //   StepInvitationCode,
      //   StepStartEndDeadline,
      //   StepLocation,
      //   StepEventTags,
      //   StepParticipationFee,
      //   StepEventContact,
      //   StepVisibility,
      // ];
    },
    id() {
      return this.$route.params.id;
    },
    maxSteps() {
      return this.isSingleStep ? 1 : this.steps.length;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    nextStep() {
      this.currentStep += 1;
    },
    prevStep() {
      this.currentStep -= 1;
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

    if (this.$route.params.step) {
      this.isSingleStep = true;
      this.currentStep = this.$route.params.step;
    }
    this.getData();
  },
};
</script>
