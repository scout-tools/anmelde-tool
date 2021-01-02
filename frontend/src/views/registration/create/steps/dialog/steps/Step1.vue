<template>
        <v-card>
      <v-card-title>
        {{ 'Neuen Teilnehmer anlegen:' }}
      </v-card-title>
      <v-card-subtitle>
        {{ 'Personenbezogenedaten' }}
      </v-card-subtitle>
      <v-card-text class="pb-0">
        <v-divider/>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-text-field
                v-model="data.firstName"
                autofocus
                :counter="20"
                :error-messages="firstNameErrors"
                label="Vorname"
                required
                @input="$v.data.firstName.$touch()"
                @blur="$v.data.firstName.$touch()"/>
            </v-row>
            <v-row>
              <v-text-field
                v-model="data.lastName"
                :counter="20"
                :error-messages="lastNameErrors"
                label="Nachname"
                required
                @input="$v.data.lastName.$touch()"
                @blur="$v.data.lastName.$touch()"/>
            </v-row>
            <v-row>
              <v-row>
                <v-dialog
                  ref="dateBirthDialog"
                  v-model="dialog.dateBirth"
                  :return-value.sync="data.dateBirth"
                  width="290px"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="dateBirthString"
                      label="Wähle das Geburtsdatum"
                      prepend-icon="mdi-clock-time-four-outline"
                      readonly
                      required
                      :error-messages="dateBirthErrors"
                      v-bind="attrs"
                      v-on="on"
                    />
                  </template>
                  <v-date-picker
                    v-if="dialog.dateBirth"
                    v-model="data.dateBirth"
                  />
                  <v-spacer/>
                  <v-card tile>
                    <v-card-actions>
                      <v-container class="py-0 px-1">
                        <v-row>
                          <v-col>
                            <v-btn
                              color="primary"
                              @click="dialog.dateBirth = false"
                              width="100%"
                            >
                              Cancel
                            </v-btn>
                          </v-col>
                          <v-col>
                            <v-btn
                              color="primary"
                              @click="$refs.dateBirthDialog.save(data.dateBirth)"
                              width="100%"
                            >
                              OK
                            </v-btn>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-row>
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
                v-model="data.city"
                :counter="20"
                :error-messages="cityErrors"
                label="Stadt"
                required
                @input="$v.data.city.$touch()"
                @blur="$v.data.city.$touch()"/>
            </v-row>
          </v-container>
        </v-form>
      </v-card-text>
    </v-card>
</template>

<script>
import {
  required, maxLength, minLength, numeric,
} from 'vuelidate/lib/validators';
import axios from 'axios';
import moment from 'moment';

export default {
  props: ['isOpen'],
  components: {
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {
      firstName: '',
      lastName: '',
      address: '',
      city: '',
      zipCode: '',
      dateBirth: '',
    },
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
