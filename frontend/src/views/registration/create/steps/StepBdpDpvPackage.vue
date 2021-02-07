<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-container>
        <p>
          Gib hier eine Adresse innerhalb Deutschlands an, wo wie ein
          Überraschungspaket für deinen Stamm hinschicken können.
        </p>

        <v-divider class="my-2" />

        <v-textarea label="Postadresse"></v-textarea>
      </v-container>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="onCloseWindow()" />
  </v-form>
</template>

<script>
import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Paketadresse',
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
  validations: {},
  watch: {
    radioGroup(value) {
      this.$store.commit('setDpvAddedLocation', value === '1');
    },
  },
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      // this.$store.commit('setDpvAddedLocation', true);
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
    beforeTabShow() {
    },
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
