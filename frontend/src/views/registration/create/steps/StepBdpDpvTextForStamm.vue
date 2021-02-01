<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="px-0" fluid>
      <p class="ma-6">
        {{ placeholder }}
      </p>
      <v-divider/>
      <v-textarea
      class="ma-6"
        label="Nachricht für den Partnerstamm"
        placeholder="Hier den Text eintippen"
      ></v-textarea>

      <v-subheader>
        Hinweis: Auch diese Nachricht kannst Du noch bis zum 01.Mai.2021
        anpassen, wenn Du sie mit deinem Stamm gemeinsam schreiben möchtest
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
import { mapGetters } from 'vuex';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Nachricht an euren Partnerstamm',
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
    placeholder: 'Hier ist Platz für eine persönliche Nachricht an euren '
    + 'noch unbekannten Partnerstamm. Wenn du Lust hast, '
    + 'dann schreibe auf, was euch ausmacht, was euer tollstes Fahrtenerlebnis war, '
    + 'euer Lieblingslied, was euch an eurer Stadt besonders gefällt… und wie man dich als '
    + 'Ansprechperson am besten erreichen kann, z.B. Mail / Whats App / Telegram / Brieftaube',
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
