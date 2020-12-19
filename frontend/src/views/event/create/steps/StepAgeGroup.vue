<template>
  <v-form
    ref="formAgeGroup"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
      <span class="subtitle-1">
        Für welche Zielgruppe(n) ist deine Aktion?
      </span>
      </v-row>
      <v-row>
        <v-select
          v-model="selectedAgeGroups"
          :items="items"
          :error-messages="selectedAgeGroupsErrors"
          item-text="name"
          item-value="id"
          label="Zielgruppe(n) wählen"
          multiple
          required
          @input="validate()"
        />
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep()" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepAgeGroup',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    items: [],
    selectedAgeGroups: [],
    API_URL: process.env.VUE_APP_API,
    valid: true,
  }),
  validations: {
    selectedAgeGroups: {
      required,
    },
  },
  computed: {
    getItems() {
      return this.items;
    },
    selectedAgeGroupsErrors() {
      const errors = [];
      if (!this.$v.selectedAgeGroups.$dirty) return errors;
      if (!this.$v.selectedAgeGroups.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    async getAgeGroups() {
      const result = await axios.get(`${this.API_URL}basic/age-group/`);
      this.items = result.data;
    },
    getData() {
      return {
        ageGroups: this.selectedAgeGroups,
      };
    },
  },
  created() {
    this.getAgeGroups();
  },
};
</script>
