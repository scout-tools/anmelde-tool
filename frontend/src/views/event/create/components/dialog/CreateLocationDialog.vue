<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    width="400px"
    persistent
  >
    <v-card>
      <v-card-title>
        {{ 'Neuen Ort anlegen:' }}
      </v-card-title>
      <v-card-subtitle>
        {{ 'Der neue Ort kann gleich direkt ausgewählt werden' }}
      </v-card-subtitle>
      <v-card-text class="pb-0">
        <v-divider/>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-text-field
                v-model="data.name"
                autofocus
                :counter="20"
                :error-messages="nameErrors"
                label="Name"
                required
                @input="$v.data.name.$touch()"
                @blur="$v.data.name.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.description"
                :counter="100"
                :error-messages="descriptionErrors"
                label="Beschreibung"
                required
                @input="$v.data.description.$touch()"
                @blur="$v.data.description.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.capacity"
                :counter="100"
                :error-messages="capacityError"
                label="Schafkapazität (unter Corona Bedinungen)"
                required
                @input="$v.data.capacity.$touch()"
                @blur="$v.data.capacity.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.address"
                :counter="30"
                :error-messages="addressErrors"
                label="Straße und Hausnummer"
                required
                @input="$v.data.address.$touch()"
                @blur="$v.data.address.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.zipCode"
                :counter="5"
                :error-messages="zipCodeErrors"
                label="Postleitzahl"
                required
                @blur="$v.data.zipCode.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.contactName"
                :counter="5"
                :error-messages="contactNameErrors"
                label="Name des Kontakts"
                required
                @blur="$v.data.contactName.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.contactEmail"
                :counter="5"
                :error-messages="contactEmailErrors"
                label="E-Mail des Kontakts"
                @blur="$v.data.contactEmail.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.contactPhone"
                :counter="5"
                :error-messages="contactPhoneErros"
                label="Telefonnummer des Kontakts"
                @blur="$v.data.contactPhone.$touch()"/>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <dialog-buttons @cancel="closeDialog()"
                        @ok="onClickOkay()"/>
      </v-card-actions>
    </v-card>
    <v-snackbar
      v-model="showError"
      color="error"
      y='top'
      :timeout="timeout"
    >
      {{ 'Fehler beim Erstellen des Ortes' }}
    </v-snackbar>
  </v-dialog>
</template>

<script>
import {
  required, maxLength, minLength, numeric,
} from 'vuelidate/lib/validators';
import axios from 'axios';
import DialogButtons from '../button/dialogButtons.vue';

export default {
  props: ['isOpen'],
  components: {
    DialogButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {
      name: '',
      description: '',
      address: '',
      zipCode: '',
      contactName: '',
      contactEmail: '',
      contactPhone: '',
      capacity: '',
    },
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
      zipCode: {
        required,
        numeric,
        minLength: minLength(5),
        maxLength: maxLength(5),
      },
      contactName: {
        required,
        maxLength: maxLength(30),
      },
      contactEmail: {
        maxLength: maxLength(30),
      },
      contactPhone: {
        maxLength: maxLength(30),
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
