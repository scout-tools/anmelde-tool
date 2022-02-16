<template>
  <v-container fluid>
    <v-card v-if="!isLoading" class="mx-auto top-margin">
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

            <v-divider :key="index" />

            <v-stepper-items :key="`stepper-items-${index}`">
              <v-stepper-content :step="index + 1">
                <component
                  :is="step"
                  :ref="step.name"
                  :position="index + 1"
                  :max-pos="steps.length"
                  :data="data"
                  @prevStep="prevStep()"
                  @nextStep="nextStep()"
                  @submit="onCreateEventClick()"
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
import axios from 'axios';
import moment from 'moment';

import StepNameDescription from './steps/StepNameDescription.vue';
import StepLocation from './steps/StepLocation.vue';
import StepAgeGroup from './steps/StepAgeGroup.vue';
import StepEventContact from './steps/StepEventContact.vue';
import StepStartEndDeadline from './steps/StepStartEndDeadline.vue';
import StepParticipationFee from './steps/StepParticipationFee.vue';
import StepInvitationCode from './steps/StepInvitationCode.vue';
import StepEventModul from './steps/StepEventModul.vue';
import StepVisibility from './steps/StepVisibility.vue';

export default {
  components: {
    StepNameDescription,
    StepLocation,
    StepAgeGroup,
    StepEventContact,
    StepStartEndDeadline,
    StepParticipationFee,
    StepInvitationCode,
    StepEventModul,
    StepVisibility,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      currentStep: 1,
      showError: false,
      showSuccess: false,
      timeout: 7000,
      isLoading: false,
      data: {
        event: {},
      },
    };
  },
  computed: {
    steps() {
      return [
        StepNameDescription,
        StepInvitationCode,
        StepStartEndDeadline,
        StepLocation,
        StepEventModul,
        StepParticipationFee,
        StepAgeGroup,
        StepEventContact,
        StepVisibility,
      ];
    },
    id() {
      return this.$route.params.id;
    },
    headerSteps() {
      return [
        'Aktionsbeschreibung',
        'Verifizierungscode',
        'Daten und Uhrzeit',
        'Ort',
        'Module',
        'Teilnehmer_innen Beitrag',
        'Zielgruppe',
        'Kontaktdaten',
        'Sichtbarkeit',
      ];
    },
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
    onSuccessfulCreateEvent() {
      setTimeout(() => this.$router.push({ name: 'eventOverview' }), 2000);
    },
    callCreateEventPost() {
      return axios.post(`${this.API_URL}basic/event/`, this.data.event);
    },
    formatCreateEventRequestData() {
      const dataNameDescription = this.$refs.StepNameDescription[0].getData();
      const dataStartEndDeadline = this.$refs.StepStartEndDeadline[0].getData();
      const dataStepLocation = this.$refs.StepLocation[0].getData();
      const dataStepEventModul = this.$refs.StepEventModul[0].getData();
      const dataStepAgeGroup = this.$refs.StepAgeGroup[0].getData();
      const dataStepEventContact = this.$refs.StepEventContact[0].getData();
      const dataStepInvitationCode = this.$refs.StepInvitationCode[0].getData();
      const dataStepParticipationFee = this.$refs.StepParticipationFee[0].getData();
      const dataStepVisibility = this.$refs.StepVisibility[0].getData();

      this.data.event = {
        name: dataNameDescription.name,
        description: dataNameDescription.description,
        location: dataStepLocation.location,
        ageGroups: dataStepAgeGroup.ageGroups,
        contact: dataStepEventContact.contacts,
        startTime: dataStartEndDeadline.startTime,
        eventTags: dataStepEventModul.eventTags,
        endTime: dataStartEndDeadline.endTime,
        registrationDeadline: dataStartEndDeadline.registrationDeadline,
        participationFee: dataStepParticipationFee.participationFee,
        invitationCode: dataStepInvitationCode.invitationCode,
        isPublic: dataStepVisibility.isPublic,
      };
    },
    async handleCreateEventRequest() {
      try {
        this.formatCreateEventRequestData();
        await this.callCreateEventPost();
        this.showSuccess = true;
        this.onSuccessfulCreateEvent();
      } catch (e) {
        console.log(e);
        this.showError = true;
      }
    },
    loadData() {
      if (this.id) {
        this.getEvent(this.id);
      }
    },
    async getEventById(id) {
      const path = `${process.env.VUE_APP_API}basic/event/${id}/`;
      const response = await axios.get(path);

      return response.data;
    },
    getEvent(id) {
      this.isLoading = true;
      Promise.all([this.getEventById(id)])
        .then((values) => {
          this.data = this.convertEvent(values[0]);

          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    toDate(value) {
      if (!value) {
        return null;
      }
      return moment(value).toDate();
    },
    convertEvent(data) {
      data.startTime = this.toDate(data.startTime); // eslint-disable-line
      data.endTime = this.toDate(data.endTime); // eslint-disable-line
      data.registrationDeadline = this.toDate(data.registrationDeadline); // eslint-disable-line
      data.registrationStart = this.toDate(data.registrationStart); // eslint-disable-line

      return data;
    },
  },
  created() {
    this.loadData();
  },
};
</script>
