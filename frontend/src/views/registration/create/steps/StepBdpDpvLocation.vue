<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <span>
            Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen (Herd/
            Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser.
          </span>
          <v-radio-group v-model="radioGroup">
            <v-radio
              label="Wir haben kein Heim/ Lagerplatz, das für das Spiel genutzt werden kann"
              value="2"
            ></v-radio>
            <v-radio
              label="Wir haben ein Heim/Lagerplatz, das für das Spiel genutzt werden kann"
              value="1"
            ></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup === '1'">
          <v-divider class="my-4" />
          <span>
            Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen (Herd/
            Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser.
          </span>
          <v-radio-group v-model="radioGroup2">
            <v-radio
              label="Wir haben einen Lagerplatz oder ein Haus, dass den Anforderungen enspricht"
              value="3"
            ></v-radio>
            <v-radio
              label="Leider entspricht unser Lagerplatz/Heim nicht den Anforderungen"
              value="5"
            ></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup2 === '3'">
          <v-divider class="my-3" />
          <span>
            Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen <br>
            (Herd/Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser. <br> <br>
          </span>
          <v-btn color="primary" @click="newLocation()">
            Platz oder Haus Hinzufügen
          </v-btn>
        </v-container>
      </v-expand-transition>
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
  displayName: 'Lagerplatz',
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
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      this.$store.commit('setDpvAddedLocation', true);
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
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
