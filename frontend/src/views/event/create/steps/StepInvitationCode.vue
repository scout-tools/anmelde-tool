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
          :error-messages="invitationCodeErrors"
          label="Verifizierungscode"
          required
          @blur="$v.data.invitationCode.$touch()"/>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep()" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { alphaNum } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

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
        alphaNum,
      },
    },
  },
  computed: {
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.data.invitationCode.$dirty) return errors;
      if (!this.$v.data.invitationCode.alphaNum) {
        errors.push('Der Einladungscode muss aus Zahlen und Buchstaben bestehen,');
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
