<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="pa-5 my-5">
      <p class="ma-6">
        {{ placeholder }}
      </p>
      <v-divider />
      <v-textarea
        class="ma-6"
        counter
        solo
        auto-grow
        prepend-icon="mdi-forum"
        label="Nachricht an die Lagerleitung"
        placeholder="Hier an die Lagerleitung"
        v-model="textfieldText"
        :error-messages="textfieldTextErrors"
      ></v-textarea>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="getEvents()" />
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { maxLength } from 'vuelidate/lib/validators';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvTextForStamm',
  displayName: 'Nachricht an die Lagerleitung',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    textfieldText: '',
    currentRegistration: [],
    placeholder:
      'Hier ist Platz für eine Nachricht an die Lagerleitung',
  }),
  computed: {
    ...mapGetters(['dpvAddedLocation']),

    textfieldTextErrors() {
      const errors = [];
      if (!this.$v.textfieldText.$dirty) return errors;
      if (!this.$v.textfieldText.maxLength) {
        errors.push('Der Text darf maximal 10000 Zeichen haben.');
      }
      return errors;
    },
  },
  validations: {
    textfieldText: {
      maxLength: maxLength(10000),
    },
  },
  watch: {
    currentRegistration() {
      if (this.currentRegistration && this.currentRegistration.length) {
        this.textfieldText = this.currentRegistration[0].freeText;
      }
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
      this.patchRegiststration().then(() => {
        this.$emit('nextStep');
      });
    },
    async patchRegiststration() {
      const registrationId = this.$route.params.id;
      return axios.patch(
        `${process.env.VUE_APP_API}basic/registration/${registrationId}/`,
        {
          freeText: this.textfieldText,
        },
      );
    },
    beforeTabShow() {
      this.loadData();
    },
    async getRegistration() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${
          this.API_URL
        }basic/registration/?id=${registrationId}&timestamp=${new Date().getTime()}`,
      );
      return res.data;
    },
    loadData() {
      this.isLoading = true;
      Promise.all([this.getRegistration()])
        .then((values) => {
          [this.currentRegistration] = values;
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
  },
};
</script>

<style>
</style>
