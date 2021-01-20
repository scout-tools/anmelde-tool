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
        <v-toolbar-title>Teilnehmer_innen hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-subheader class="ma-5">
          Bitte trag hier die Daten ein die das Anmeldetool aus. Diese Daten
          werden teilweise später in Anwendungen gebraucht. Diese Daten sind für
          die Administratoren und für die Lagerleitung nach deiner explizieten
          Anmeldung sichtbar.
        </v-subheader>
        <v-form v-model="valid">
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-combobox
                v-model="data.group"
                :items="items"
                item-text="name"
                item-value="id"
                autofocus
                label="Gruppe"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-checkbox v-model="data.groupleader" label="Gruppenführung" />
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.firstName"
                :counter="20"
                :error-messages="firstNameErrors"
                label="Vorname"
                required
                @input="$v.data.firstName.$touch()"
                @blur="$v.data.firstName.$touch()"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.lastName"
                :counter="20"
                :error-messages="lastNameErrors"
                label="Nachname"
                required
                @input="$v.data.lastName.$touch()"
                @blur="$v.data.lastName.$touch()"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-row>
               <birthday-field/>
              </v-row>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.street"
                :counter="30"
                :error-messages="streetErrors"
                label="Straße und Hausnummer"
                required
                @input="$v.data.street.$touch()"
                @blur="$v.data.street.$touch()"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <zip-code-field />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <eat-field />
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-checkbox
                v-model="data.mosaikersleben"
                label="Nimmt an der Bundesfahrt teil"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-checkbox
                v-model="data.kaperfahrt"
                label="Nimmt an der Kaperfahrt teil"
              />
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

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
import moment from 'moment';

import ZipCodeField from '@/components/field/ZipCodeField.vue';
import EatField from '@/components/field/EatField.vue';
import BirthdayField from '@/components/field/BirthdayField.vue';

export default {
  props: ['isOpen'],
  components: {
    ZipCodeField,
    EatField,
    BirthdayField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {
      firstName: '',
      lastName: '',
      street: '',
      city: '',
      zipCode: '',
      dateBirth: '',
      groupLeader: false,
      kaperfahrt: false,
      mosaikersleben: true,
      registration: 0,
    },
    items: [
      {
        id: 1,
        name: 'Bären',
      },
      {
        id: 2,
        name: 'Döner',
      },
    ],
    dialog: {
      dateBirth: false,
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {
    data: {
      firstName: {
        required,
        maxLength: maxLength(20),
      },
      lastName: {
        required,
        maxLength: maxLength(20),
      },
      dateBirth: {
        required,
        maxLength: maxLength(10),
      },
      street: {
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
    firstNameErrors() {
      const errors = [];
      if (!this.$v.data.firstName.$dirty) return errors;
      if (!this.$v.data.firstName.required) {
        errors.push('Name is required.');
      }
      if (!this.$v.data.firstName.maxLength) {
        errors.push('Name must be at most 20 characters long');
      }
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.data.lastName.$dirty) return errors;
      if (!this.$v.data.lastName.required) {
        errors.push('Name is required.');
      }
      if (!this.$v.data.lastName.maxLength) {
        errors.push('Name must be at most 20 characters long');
      }
      return errors;
    },
    dateBirthErrors() {
      const errors = [];
      if (!this.$v.data.dateBirth.$dirty) return errors;
      if (!this.$v.data.dateBirth.required) {
        errors.push('Geburtstag is required.');
      }
      if (!this.$v.data.dateBirth.maxLength) {
        errors.push('Geburtstag must be at most 10 characters long');
      }
      return errors;
    },
    dateBirthString() {
      const dateFormat = 'DD.MM.YYYY';
      if (this.data.dateBirth === '') {
        return '';
      }
      return `${moment(this.data.dateBirth).format(dateFormat)}`;
    },
    streetErrors() {
      const errors = [];
      if (!this.$v.data.street.$dirty) return errors;
      if (!this.$v.data.street.required) {
        errors.push('Adresse is required.');
      }
      if (!this.$v.data.street.maxLength) {
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
          this.callCreateParticipantPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateParticipantPost() {
      this.data.registration = this.$route.params.id;
      await axios.post(`${this.API_URL}basic/participant-personal/`, this.data);
    },
    getData() {
      return this.data;
    },
  },
};
</script>
