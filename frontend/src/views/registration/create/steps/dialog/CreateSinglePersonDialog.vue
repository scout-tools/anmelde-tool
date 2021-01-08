<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Neuen Teilnehmer hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-stepper v-model="e1" fullscreen>
        <v-stepper-header>
          <v-stepper-step :complete="e1 > 1" step="1">
            Persönliches
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step :complete="e1 > 2" step="2"> Essen </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step step="3"> Teilnahme </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items class="fullscreen">
          <v-stepper-content step="1">
            <v-container>
              <step-1 />
              <step-2 />
              <v-divider class="my-4"/>
              <v-btn color="primary" @click="active = false"> Speichern </v-btn>
            </v-container>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Erstellen des Ortes' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required,
  maxLength,
  minLength,
  numeric,
} from 'vuelidate/lib/validators';
import axios from 'axios';
import Step1 from './steps/Step1.vue';
import Step2 from './steps/Step2.vue';

export default {
  props: ['isOpen'],
  components: {
    Step1,
    Step2,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {
      name: '',
      description: '',
      address: '',
      city: '',
      zipCode: '',
    },
    e1: 1,
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {
    data: {
      name: {
        required,
        maxLength: maxLength(20),
      },
      description: {
        maxLength: maxLength(100),
      },
      address: {
        required,
        maxLength: maxLength(30),
      },
      city: {
        required,
        maxLength: maxLength(20),
      },
      zipCode: {
        required,
        numeric,
        minLength: minLength(5),
        maxLength: maxLength(5),
      },
    },
  },
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.data.name.$dirty) return errors;
      if (!this.$v.data.name.required) {
        errors.push('Name is required.');
      }
      if (!this.$v.data.name.maxLength) {
        errors.push('Name must be at most 20 characters long');
      }
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.data.description.$dirty) return errors;
      if (!this.$v.data.description.maxLength) {
        errors.push('description must be at most 100 characters long');
      }
      return errors;
    },
    addressErrors() {
      const errors = [];
      if (!this.$v.data.address.$dirty) return errors;
      if (!this.$v.data.address.required) {
        errors.push('Adresse is required.');
      }
      if (!this.$v.data.address.maxLength) {
        errors.push('Adresse must be at most 20 characters long');
      }
      return errors;
    },
    cityErrors() {
      const errors = [];
      if (!this.$v.data.city.$dirty) return errors;
      if (!this.$v.data.city.required) {
        errors.push('Stadt is required.');
      }
      if (!this.$v.data.city.maxLength) {
        errors.push('Stadt must be at most 30 characters long');
      }
      return errors;
    },
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.data.zipCode.$dirty) return errors;
      if (!this.$v.data.zipCode.required) {
        errors.push('PLZ is required.');
      }
      if (!this.$v.data.zipCode.numeric) {
        errors.push('PLZ muss eine Zahl sein.');
      }
      if (!this.$v.data.zipCode.minLength || !this.$v.data.zipCode.maxLength) {
        errors.push('PLZ muss eine 5-stellige Zahl sein.');
      }
      return errors;
    },
  },
  methods: {
    onClickOk() {
      this.active = false;
    },
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.active = true;
    },
    closeDialog() {
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateEventLocationPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateEventLocationPost() {
      await axios.post(`${this.API_URL}basic/event-location/`, this.data);
    },
  },
};
</script>

<style>
.fullscreen {
  height: 100% !important;
}
</style>
