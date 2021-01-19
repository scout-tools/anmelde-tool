<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
  <v-container
    class="px-0"
    fluid
  >
        <v-textarea
          name="input-7-1"
          label="Text für den Partnerstamm"
        ></v-textarea>

<v-expand-transition>
  <v-checkbox
    v-show="dpvAddedLocation"
    v-model="data.checkbox1"
    :label="`Wir stellen unser Heim / Lagerplatz anderen Stämmen zur Verfügung.)`"/>
  <v-divider class="my-3" />
</v-expand-transition>

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
  </v-container>
  <create-location-dialog ref="newLocationDialog" @close="getEvents()"/>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Nachricht an Partnerstamm',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    radioGroup: 0,
    radioGroup2: 0,
    data: {
      value1: true,
      value2: false,
    },
  }),
  computed: {
    ...mapGetters(['dpvAddedLocation']),
  },
  validations: {},
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
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
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
  },
};
</script>

<style>
</style>
