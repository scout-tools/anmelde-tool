<template>
  <v-form
    ref="formEventContact"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-2">
      <span class="subtitle-1">
        Trage hier deine Kontaktdaten als Ansprechpartner ein.
      </span>
      </v-row>
      <v-row class="ma-4">
        <v-text-field
          outlined
          autofocus
          :counter="30"
          :rules="rules.name"
          label="Name"
          v-model="data.name"
          required>
        </v-text-field>
      </v-row>
      <v-row class="ma-4">
        <v-text-field
          outlined
          :error-messages="emailError"
          :rules="rules.email"
          label="E-Mail-Adresse"
          v-model="data.email"
          required>
        </v-text-field>
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { validationMixin } from 'vuelidate';
import { email, required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  mixins: [validationMixin],
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      name: '',
      email: '',
    },
    validators: {
      email: {
        required,
        email,
      },
    },
    rules: {
      name: [
        (v) => !!v || 'Name ist erforderlich.',
        (v) => (v && v.length <= 30) || 'Der Name ist zu lang.',
      ],
      email: [
        (v) => !!v || 'E-Mail-Adresse ist erforderlich.',
      ],
    },
  }),
  computed: {
    emailError() {
      return []; // TODO EMail validierung
    },
  },
  methods: {
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.$refs.formEventContact.validate()) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      if (!this.$refs.formEventContact.validate()) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
