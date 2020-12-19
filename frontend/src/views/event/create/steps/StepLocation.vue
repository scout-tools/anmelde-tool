<template>
  <v-form
    ref="formLocation"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
          Trage hier den Namen von dem Ort ein.
        </span>
      </v-row>
      <v-row>
        <v-select
          v-model="selectedLocation"
          :items="items"
          :error-messages="selectedLocationErrors"
          item-text="preview"
          item-value="id"
          label="Veranstaltungsort wählen"
          required
          @input="validate()"
        />
      </v-row>

      <v-divider class="my-2"/>
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepLocation',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    items: [],
    selectedLocation: null,
    API_URL: process.env.VUE_APP_API,
    valid: true,
  }),
  validations: {
    selectedLocation: {
      required,
    },
  },
  computed: {
    selectedLocationErrors() {
      const errors = [];
      if (!this.$v.selectedLocation.$dirty) return errors;
      if (!this.$v.selectedLocation.required) {
        errors.push('Es muss ein Veranstaltungsort ausgewählt werden.');
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
    async getEvents() {
      const result = await axios.get(`${this.API_URL}basic/event-location/`);
      this.items = result.data;
      this.formatLocationPreview();
    },
    formatLocationPreview() {
      this.items = this.items.map(({
        name, zipCode, city, address, ...args
      }) => ({
        preview: `${name}: ${zipCode} ${city} (${address})`,
        ...args,
      }));
    },
    getData() {
      return {
        location: this.selectedLocation,
      };
    },
  },
  created() {
    this.getEvents();
  },
};
</script>
