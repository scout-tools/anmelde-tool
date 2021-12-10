<template>
  <v-form ref="formAgeGroup" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
          Für welche Zielgruppe(n) ist deine Aktion?
        </span>
      </v-row>
      <v-row>
        <v-select
          v-model="data.ageGroups"
          :items="ageGroupList"
          :error-messages="ageGroupsErrors"
          item-text="name"
          item-value="id"
          label="Zielgruppe(n) wählen"
          multiple
          required
          @input="validate()"
        />
      </v-row>

      <v-divider class="my-2" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep()"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepAgeGroup',
  props: ['position', 'maxPos', 'data'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    items: [],
    ageGroupList: [],
    API_URL: process.env.VUE_APP_API,
    valid: true,
  }),
  validations: {
    data: {
      ageGroups: {
        required,
      },
    },
  },
  computed: {
    getItems() {
      return this.items;
    },
    ageGroupsErrors() {
      const errors = [];
      if (!this.$v.data.ageGroups.$dirty) return errors;
      if (!this.$v.data.ageGroups.required) {
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
      const result = await axios.get(`${this.API_URL}/basic/age-group/`);
      this.ageGroupList = result.data;
    },
    getData() {
      return {
        ageGroups: this.data.ageGroups,
      };
    },
  },
  created() {
    this.getAgeGroups();
  },
};
</script>
