<template>
  <v-container>
    <v-row justify="center">
      <v-flex
        ma-3
        lg7
      >
        <v-stepper
          alt-labels
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
                :ref="step"
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
// import axios from 'axios';

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

    finish() {
      /*
         const dataStep1 = this.$refs.step1.getData();
         const dataStep2 = this.$refs.step2.getData();
         const dataStep3 = this.$refs.step3.getData();
         const dataStep4 = this.$refs.step4.getData();
         const dataStep5 = this.$refs.step5.getData();
         const dataStep6 = this.$refs.step6.getData();
         const dataStep7 = this.$refs.step7.getData();
         if (this.isCreate) {
           axios.post(`${this.API_URL}basic/event/`, {
             title: dataStep1.title,
             description: dataStep2.description,
             tags: this.getUrlTagList(dataStep5.tags.concat(dataStep6.selectedMandatoryFilter)),
             material: this.convertMaterialArray(dataStep3.material),
             costsRating: dataStep4.costsRating,
             executionTimeRating: dataStep4.executionTimeRating,
             isPrepairationNeeded: dataStep4.isPrepairationNeeded,
             isActive: dataStep7.isActive,
             createdBy: dataStep7.createdBy,
             createdByEmail: dataStep7.createdByEmail,
           })
             .then(() => {
               this.$router.push({ name: 'overview', params: { showSuccess: true } });
             })
             .catch(() => {
               this.showError = true;
             });
         } else if (this.isUpdate) {
           axios.put(`${this.API_URL}basic/event/${this.getId}/`, {
             id: this.data.id,
             title: dataStep3.title,
             description: dataStep2.description,
             tags: this.getUrlTagList(dataStep5.tags.concat(dataStep6.selectedMandatoryFilter)),
             material: this.convertMaterialArray(dataStep3.material),
             costsRating: dataStep4.costsRating,
             executionTimeRating: dataStep5.executionTimeRating,
             isPrepairationNeeded: dataStep6.isPrepairationNeeded,
             isActive: dataStep7.isActive,
             createdBy: dataStep7.createdBy,
             createdByEmail: dataStep7.createdByEmail,
           })
             .then(() => {
               this.$router.push({ name: 'overview' });
               this.$emit('dialogClose');
               this.showSuccess = true;
             })
             .catch(() => {
               this.showError = true;
             });
         } */
    },
  },
};
</script>
