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
            <template v-for="(step, index) in steps">
              <v-stepper-step
                :key="`${index+1}-step`"
                :complete="currentStep > index+1"
                :step="index+1"
              >
                {{ headerStep[index] }}
              </v-stepper-step>

              <v-divider
                v-if="index !== index"
                :key="index-1"
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
                @prevStep="prevStep()"
                @nextStep="nextStep()"
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

import StepNameBeschreibung from './steps/StepNameBeschreibung.vue';
import StepLocation from './steps/StepLocation.vue';

export default {
  components: {
    StepNameBeschreibung,
    StepLocation,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      currentStep: 1,
      steps: [StepNameBeschreibung, StepLocation, StepNameBeschreibung],
      showError: false,
      showSuccess: false,
      timeout: 7000,
      headerStep: [
        'StepAnAbreise',
        'StepLocation',
        'StepAnAbreise2',
      ],
      data: [],
    };
  },

  computed: {
    isCreate() {
      return !this.$route.params.id;
    },
    isUpdate() {
      return !!this.$route.params.id;
    },
    getId() {
      return this.$route.params.id;
    },
  },

  watch: {
    steps(val) {
      if (this.currentStep > val) {
        this.currentStep = val;
      }
    },
  },

  methods: {
    nextStep() {
      this.currentStep += 1;
    },
    prevStep() {
      this.currentStep -= 1;
    },

    /* finish() {
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
      }
    }, */
  },
};
</script>
