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
                v-model="data.scoutGroup"
                :items="scoutHierarchyGroups"
                item-text="name"
                item-value="name"
                autofocus
                required
                :rules="[requiredField]"
                label="Gruppe"
                prepend-icon="mdi-account-group"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-combobox>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-switch v-model="data.isGroupLeader" label="Gruppenführung">
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-switch>
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
                prepend-icon="mdi-card-account-details-outline"
                @input="$v.data.firstName.$touch()"
                @blur="$v.data.firstName.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.lastName"
                :counter="20"
                :error-messages="lastNameErrors"
                label="Nachname"
                required
                prepend-icon="mdi-card-account-details-outline"
                @input="$v.data.lastName.$touch()"
                @blur="$v.data.lastName.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                label="Alter"
                v-model="data.age"
                type="number"
                suffix="Jahre"
                :error-messages="ageErrors"
                prepend-icon="mdi-human-child"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Alter zum Lagerbeginn' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.street"
                :counter="30"
                :error-messages="streetErrors"
                label="Straße und Hausnummer"
                prepend-icon="mdi-home"
                required
                @input="$v.data.street.$touch()"
                @blur="$v.data.street.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.phoneNumber"
                :counter="30"
                :error-messages="phoneNumberErrors"
                label="Telefonnummer"
                prepend-icon="mdi-phone"
                required
                @input="$v.data.phoneNumber.$touch()"
                @blur="$v.data.phoneNumber.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ 'Gallo' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <zip-code-field ref="zipCodeField" v-model="data.zipCode" />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <eat-field ref="eatHabitType" v-model="data.eatHabitType" />
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-row>
            <v-col cols="12" sm="6">
              <v-container fluid>
                <v-select
                  v-model="data.participantRole"
                  prepend-icon="mdi-tent"
                  :items="roleItems"
                  :error-messages="participantRoleErrors"
                  item-text="name"
                  item-value="id"
                  label="Bundesfahrt und/oder Kaperfahrt?"
                  required
                  @input="validate()"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Gallo' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-select>
              </v-container>
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ 'Gallo' }}
                  </span>
                </v-tooltip>
              </template>
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
import { required, maxLength, numeric } from 'vuelidate/lib/validators';
import axios from 'axios';
import moment from 'moment';
import { mapGetters } from 'vuex';

import ZipCodeField from '@/components/field/ZipCodeField.vue';
import EatField from '@/components/field/EatField.vue';

export default {
  props: ['isOpen'],
  components: {
    ZipCodeField,
    EatField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    scoutHierarchyGroups: [],
    data: {
      firstName: null,
      lastName: null,
      street: null,
      zipCode: null,
      phoneNumber: null,
      age: null,
      registration: null,
      eatHabitType: [],
      scoutGroup: null,
      isGroupLeader: false,
      participantRole: 6,
    },
    roleItems: [
      {
        id: 6,
        name: 'Nur Bundesfahrt',
      },
      {
        id: 7,
        name: 'Bundesfahrt + Kaperfahrt',
      },
    ],
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
      scoutGroup: {
        required,
      },
      phoneNumber: {
        required,
      },
      age: {
        required,
      },
      street: {
        required,
        maxLength: maxLength(30),
      },
      zipCode: {
        required,
        numeric,
      },
      participantRole: {
        required,
      },
    },
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping']),
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
    scoutGroupsErrors() {
      const errors = [];
      if (!this.$v.data.scoutGroup.$dirty) return errors;
      if (!this.$v.data.scoutGroup.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
    ageErrors() {
      const errors = [];
      if (!this.$v.data.age.$dirty) return errors;
      if (!this.$v.data.age.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
    phoneNumberErrors() {
      const errors = [];
      if (!this.$v.data.phoneNumber.$dirty) return errors;
      if (!this.$v.data.phoneNumber.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
    participantRoleErrors() {
      const errors = [];
      if (!this.$v.data.participantRole.$dirty) return errors;
      if (!this.$v.data.participantRole.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
  },
  watch: {
    data() {
      this.$refs.zipCodeField.setValue(this.data.zipCode);
      this.$refs.eatHabitType.setValue(this.data.eatHabitType);
    },
  },
  methods: {
    refresh() {},
    requiredField(value) {
      if (value instanceof Array && value.length === 0) {
        return 'Bitte Füllen';
      }
      return !!value || 'Bitte Füllen';
    },
    onClickOk() {
      this.active = false;
    },
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.data = {
        firstName: null,
        lastName: null,
        street: null,
        zipCode: null,
        phoneNumber: null,
        age: 3,
        registration: null,
        eatHabitType: [],
        scoutGroup: null,
        isGroupLeader: false,
        participantRole: 6,
      };
      this.active = true;
      this.getGroups();
    },
    openDialogEdit(input) {
      this.data = input;
      this.active = true;
      this.getGroups();
    },
    getGroups() {
      axios
        .get(`${this.API_URL}basic/scout-hierarchy-group/`)
        .then((res) => {
          this.scoutHierarchyGroups = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    getParticipantPersonalById(id) {
      axios
        .get(`${this.API_URL}basic/participant-personal/${id}/`)
        .then((res) => {
          this.data = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
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
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateParticipantPost() {
      this.data.registration = this.$route.params.id;
      if (this.data.scoutGroup && this.data.scoutGroup.name) {
        this.data.scoutGroup = this.data.scoutGroup.name;
      }
      if (this.data.eatHabitType && this.data.eatHabitType.name) {
        this.data.eatHabitType = this.data.eatHabitType.name;
      }
      if (!this.data.id) {
        axios
          .post(`${this.API_URL}basic/participant-personal/`, this.data)
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      } else {
        axios
          .put(
            `${this.API_URL}basic/participant-personal/${this.data.id}/`,
            this.data,
          )
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      }
    },
    getData() {
      return this.data;
    },
  },
};
</script>
