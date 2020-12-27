<template>
  <v-form
    ref="formNameDescription"
    v-model="valid"
  >
    <v-container>
      <v-row class="mb-6">
      <span class="subtitle-1">
        Lege für die Aktion einen 6-Stelligen Verifizierungscode fest. <br>
        Dieser besteht aus Buchstaben und Zahlen und wird bei der Anmeldung mitgeschickt,
        damit sich die Anmelder verifizieren können, dass sie eingeladen wurden. <br>
        Bei leerem Feld gibt es keinen Verifizierungscode.
      </span>
      </v-row>
      <v-row>
        <v-text-field
          v-model="data.invitationCode"
          :counter="6"
          :error-messages="invitationCodeErrors"
          label="Verifizierungscode"
          required
          @blur="$v.data.invitationCode.$touch()">
        </v-text-field>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { alphaNum } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

const emptyOrLengthSix = (value) => value.length === 6 || value.length === 0;

export default {
  name: 'StepInvitationCode',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      invitationCode: '',
    },
  }),
  validations: {
    data: {
      invitationCode: {
        emptyOrLengthSix,
        alphaNum,
      },
    },
  },
  computed: {
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.data.invitationCode.$dirty) return errors;
      // TODO Umlaute und ß funktionieren nicht => erstmal ignorieren?
      if (!this.$v.data.invitationCode.alphaNum) {
        errors.push('Der Einladungscode muss aus Zahlen und Buchstaben bestehen,');
      }
      if (!this.$v.data.invitationCode.emptyOrLengthSix) {
        errors.push('Der Einladungscode muss entweder leer sein oder aus 6 Stellen bestehen.');
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
    getData() {
      return {
        invitationCode: this.data.invitationCode,
      };
    },
  },
};
</script>

<style scoped>

</style>
