<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <span>
            <b
              >Das Heim/Der Lagerplatz meines Stammes kann für die Aktion
              genutzt werden
            </b>
            <br />
            <br />
            Notwendig sind:
            <ul>
              <li>Möglichkeiten zum Kochen (Herd/Feuerstelle)</li>
              <li>ausreichend Toiletten und fließend Wasser</li>
            </ul>
          </span>
          <v-radio-group v-model="radioGroup">
            <v-radio
              label="Nein"
              value="2"
            ></v-radio>
            <v-radio
              label="Ja"
              value="1"
            ></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup === '1'">
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
  displayName: 'Unser Heim/Lagerplatz',
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
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
