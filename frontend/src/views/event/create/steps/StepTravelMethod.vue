<template>
  <v-form
    ref="formTravelMethod"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
      <span class="subtitle-1">
        Wie darf man zu der Veranstaltung anreisen?
      </span>
      </v-row>
      <v-row>
        <v-select
          v-model="selectedTravelMethods"
          :items="items"
          :error-messages="selectedTravelMethodsErrors"
          item-text="name"
          item-value="id"
          label="Reisemöglichkeit(en) wählen"
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
  name: 'StepTravelMethod',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    items: [],
    selectedTravelMethods: [],
    API_URL: process.env.VUE_APP_API,
    valid: true,
  }),
  validations: {
    selectedTravelMethods: {
      required,
    },
  },
  computed: {
    getItems() {
      return this.items;
    },
    selectedTravelMethodsErrors() {
      const errors = [];
      if (!this.$v.selectedTravelMethods.$dirty) return errors;
      if (!this.$v.selectedTravelMethods.required) {
        errors.push('Es muss mindestens eine Methode ausgewählt werden.');
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
    async getTravelMethods() {
      const result = await axios.get(`${this.API_URL}basic/travel-method/`);
      this.items = result.data;
    },
    getData() {
      return {
        TravelMethods: this.selectedTravelMethods,
      };
    },
  },
  created() {
    this.getTravelMethods();
  },
};
</script>
