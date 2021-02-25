<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="px-0">
      <p class="ma-6">
        {{ placeholder }}
      </p>
      <v-divider />
      <v-textarea
        class="ma-6"
        label="Nachricht für den Partnerstamm"
        placeholder="Hier den Text eintippen"
        v-model="textfieldText"
      ></v-textarea>

      <v-subheader>
        Hinweis: Auch diese Nachricht kannst Du noch bis zum 01.Mai.2021
        anpassen, wenn Du sie mit deinem Stamm gemeinsam schreiben möchtest.
      </v-subheader>
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

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvTextForStamm',
  displayName: 'Nachricht an euren Partnerstamm',
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
      'Hier ist Platz für eine persönliche Nachricht an euren ' + // eslint-disable-line
      'noch unbekannten Partnerstamm. Wenn du Lust hast, ' + // eslint-disable-line
      'dann schreibe auf, was euch ausmacht, was euer tollstes Fahrtenerlebnis war, ' + // eslint-disable-line
      'euer Lieblingslied, was euch an eurer Stadt besonders gefällt und wie man dich als ' + // eslint-disable-line
      'Ansprechperson am besten erreichen kann, z.B. Mail / Whats App / Telegram / Brieftaube.', // eslint-disable-line
  }),
  computed: {
    ...mapGetters(['dpvAddedLocation']),
  },
  validations: {},
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
      this.patchRegiststration().then((item) => {
        console.log(item);
        this.$emit('nextStep');
      });
    },
    async patchRegiststration() {
      const registrationId = this.$route.params.id;
      return axios.patch(`${process.env.VUE_APP_API}basic/registration/${registrationId}/`, {
        freeText: this.textfieldText,
      });
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
