<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <v-row v-if="dpvAddedLocation">
            <p>Sehr cool. Du hast ein Heim / Lagerplatz hinzugefügt.</p>
            <v-radio-group v-model="radioGroup">
              <v-radio
                label="Wir wollen bei uns im Heim bleiben und besucht werden."
                value="1"
              ></v-radio>
              <v-radio
                label="Wir wollen einen anderen Stamm besuchen
                und stellen unser Heim zur Verfügung."
                value="2"
              ></v-radio>
              <v-radio label="Uns ist beides recht." value="3"></v-radio>
            </v-radio-group>
          </v-row>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container
          v-show="!dpvAddedLocation || radioGroup === '2' || radioGroup === '3'"
        >
          <v-divider class="my-4" />
          <v-radio-group v-model="radioGroup2">
            <v-radio
              label="Wir möchten gern in der Nähe unserer Stadt bleiben.
              (Mit der Regio kommt man gut hin) "
              value="5"
            ></v-radio>
            <v-radio
              label="Wir fahren gern weit weg.
              (Im Zweifel quer durch ganz Deutschland) "
              value="3"
            >
            </v-radio>
            <v-radio label="Uns ist beides recht." value="6"></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <p
        class="text-center"
        v-if="radioGroup2 !== 0"
        style="border-style: solid; border-color: red"
      >
        <v-icon color="pink darken-1" large class="ma-2">
          mdi-unicorn mdi-spin
        </v-icon>
        {{ textSnackbar }}
        <v-icon color="pink darken-1" large class="ma-2">
          mdi-unicorn mdi-flip-h mdi-spin
        </v-icon>
      </p>

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
  displayName: 'Wohin geht es?',
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
    snackbar: false,
    textSnackbar:
      'Wir geben uns größte Mühe alles zu beachten, aber können nichts versprechen. ',
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
      this.snackbar = true;
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
    beforeTabShow() {},
  },
};
</script>

<style>
</style>
