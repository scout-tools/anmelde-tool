<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="pa-5 my-5">
      <v-row class="mt-2">
        <!-- <span class="text-left subtitle-1">
          <p><b>Zusammenfassung</b></p>
            Ich habe folgende Daten eingefügt:
        </span> -->
      </v-row>
      <!-- <v-divider class="text-left my-2" /> -->
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="
            `Ich habe meine Daten überprüft und sende diese ` +
            `Anmeldung verbindlich an die Lagerleitung.`
          "
          :error-messages="checkbox1Errors"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '@/components/button/PrevNextButton.vue';

export default {
  name: 'StepConfirm',
  displayName: 'Zusammenfassung und Bestätigung',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      checkbox1: false,
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
    id() {
      return this.$route.params.id;
    },
    checkbox1Errors() {
      const errors = [];
      if (!this.$v.data.checkbox1.$dirty) return errors;
      if (!this.$v.data.checkbox1.required || !this.$v.data.checkbox1.checked) {
        errors.push(
          'Deine Zustimmung ist erforderlich, damit du dich anmelden kannst.',
        );
      }
      return errors;
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
