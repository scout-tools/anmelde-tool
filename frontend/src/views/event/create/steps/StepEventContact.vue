<template>
  <v-form
    ref="formEventContact"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
      <span class="subtitle-1">
        {{'Trage hier die E-Mail-Adressen der verantwortlichen Kontaktpersonen ' +
          ' als Ansprechperson ein.' }}
        <br>
        <i>{{' (Jede geschriebene E-Mail-Adresse muss mit Enter bestätigt werden!)'}}</i>
      </span>
      </v-row>
      <v-row>
        <v-combobox
          :error-messages="contactsErrors"
          autofocus
          v-model="contacts"
          label="verantwortliche Kontaktpersonen"
          multiple
          required
          small-chips
          deletable-chips
          chips
        />
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep()" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required, email } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepEventContact',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    contacts: [],
  }),
  validations: {
    contacts: {
      required,
      $each: {
        email,
      },
    },
  },
  computed: {
    contactsErrors() {
      const errors = [];
      if (!this.$v.contacts.$dirty) return errors;
      if (!this.$v.contacts.required) {
        errors.push('Es muss mindestens eine Ansprechperson angegeben werden.');
      }
      if (this.$v.contacts.$each.$anyError) {
        errors.push('Es müssen gültige E-Mail-Adressen angegeben werden.');
      }
      return errors;
    },
  },
  methods: {
    validate() {
      this.$v.contacts.$touch();
      this.valid = !this.$v.contacts.$anyError;
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
        contacts: this.contacts,
      };
    },
  },
};
</script>
