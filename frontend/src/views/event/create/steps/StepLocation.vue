<template>
  <v-form
    ref="formLocation"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
          {{ 'Wähle hier den Veranstaltungsort aus.' }}
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
      <v-row>
        <p class="mr-4">
          {{ 'Oder erstelle zuerst einen neuen Ort:' }}
        </p>
        <v-btn
          small
          color="secondary"
          @click="newLocation()">
          {{ 'Neuen Ort anlegen' }}
        </v-btn>
        <create-location-dialog ref="newLocationDialog" @close="getEvents()"/>
      </v-row>
      <v-divider class="my-4"/>
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep()" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import CreateLocationDialog from '../components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepLocation',
  props: ['position', 'maxPos', 'data'],
  components: {
    CreateLocationDialog,
    PrevNextButtons,
  },
  data: () => ({
    items: [],
    selectedLocation: null,
    locationDialog: false,
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
      const url = `${this.API_URL}basic/event-location/?&timestamp=${new Date().getTime()}`;
      const result = await axios.get(url);
      this.items = result.data;
      this.formatLocationPreview();
    },
    formatLocationPreview() {
      this.items = this.items.map(({
        name, description, address, ...args
      }) => ({
        preview: `${name}: ${description} (${address})`,
        ...args,
      }));
    },
    getData() {
      return {
        location: this.selectedLocation,
      };
    },
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
  },
  created() {
    this.getEvents();
  },
};
</script>
