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
                :rules="[requiredField, validScoutGroup]"
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
                      {{ 'Gruppe des Teilnehmenden aus der Liste auswählen ' +
                          'oder neuen Namen eingeben' }}
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
                      {{ 'Ist Teil der Gruppenführung der Gruppe' }}
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
                      {{ 'Vorname des Teilnehmenden' }}
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
                      {{ 'Nachname des Teilnehmenden' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.age"
                :error-messages="ageErrors"
                label="Alter"
                suffix="Jahre"
                prepend-icon="mdi-human-child"
                required
                @input="$v.data.age.$touch()"
                @blur="$v.data.age.$touch()"
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
                      {{ 'Adresse des Teilnehmenden' }}
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
                      {{ 'Telefonnummer des Teilnehmenden' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <zip-code-field ref="zipCodeField" v-model="data.zipCode" />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <eat-autocomplete-field ref="eatHabitType" v-model="data.eatHabitType" />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <eat-text-field ref="eatHabitText" v-model="eatHabitText" />
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
                  @input="$v.data.participantRole.$touch()"
                >
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                    {{ 'An welchen Teilfahrten nimmt der Teilnehmende teil?' }}
                  </span>
                    </v-tooltip>
                  </template>
                </v-select>
              </v-container>
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Anlegen eines Teilnehmenden' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required, minLength, maxLength, integer, minValue,
} from 'vuelidate/lib/validators';
import axios from 'axios';
// import moment from 'moment';
import { mapGetters } from 'vuex';

import ZipCodeField from '@/components/field/ZipCodeField.vue';
import EatAutocompleteField from '@/components/field/EatAutocompleteField.vue';
import EatTextField from '@/components/field/EatTextField.vue';

const scoutGroupStartValidator = (groupObjOrGroupName) => {
  const validStarts = ['Meute', 'Sippe', 'Roverrunde'];
  if (!groupObjOrGroupName) {
    return false;
  }
  const name = (groupObjOrGroupName.name) ? groupObjOrGroupName.name : groupObjOrGroupName;
  return validStarts.includes(name.trim().split(' ')[0]);
};

export default {
  props: ['isOpen'],
  components: {
    ZipCodeField,
    EatAutocompleteField,
    EatTextField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    scoutHierarchyGroups: [],
    eatHabitText: null,
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
        id: 5,
        name: 'Nur Bundesfahrt',
      },
      {
        id: 6,
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
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      lastName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      scoutGroup: {
        required,
        scoutGroupStartValidator,
      },
      phoneNumber: {
        required,
        integer,
        minValue: minValue(1),
      },
      age: {
        required,
        integer,
        minValue: minValue(1),
      },
      street: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(30),
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
        errors.push('Vorname ist erforderlich.');
      }
      if (!this.$v.data.firstName.minLength) {
        errors.push('Vorname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.firstName.maxLength) {
        errors.push('Vorname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.data.lastName.$dirty) return errors;
      if (!this.$v.data.lastName.required) {
        errors.push('Nachname ist erforderlich.');
      }
      if (!this.$v.data.lastName.minLength) {
        errors.push('Nachname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.lastName.maxLength) {
        errors.push('Nachname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    streetErrors() {
      const errors = [];
      if (!this.$v.data.street.$dirty) return errors;
      if (!this.$v.data.street.required) {
        errors.push('Adresse ist erforderlich.');
      }
      if (!this.$v.data.street.minLength) {
        errors.push('Adresse muss mindestens 5 Zeichen lang sein.');
      }
      if (!this.$v.data.street.maxLength) {
        errors.push('Adresse darf maximal 30 Zeichen lang sein.');
      }
      return errors;
    },
    scoutGroupsErrors() {
      const errors = [];
      if (!this.$v.data.scoutGroup.$dirty) return errors;
      if (!this.$v.data.scoutGroup.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      if (!this.$v.data.scoutGroup.scoutGroupStartValidator) {
        errors.push('Der Gruppenname muss mit Meute, Sippe oder Roverrunde beginnen.');
      }
      return errors;
    },
    ageErrors() {
      const errors = [];
      if (!this.$v.data.age.$dirty) return errors;
      if (!this.$v.data.age.required) {
        errors.push('Alter ist erforderlich.');
      }
      if (!this.$v.data.age.integer || !this.$v.data.age.minValue) {
        errors.push('Es muss ein gültiges Alter eingetragen werden.');
      }
      return errors;
    },
    phoneNumberErrors() {
      const errors = [];
      if (!this.$v.data.phoneNumber.$dirty) return errors;
      if (!this.$v.data.phoneNumber.required) {
        errors.push('Telefonnummer ist erforderlich.');
      }
      if (!this.$v.data.phoneNumber.integer || !this.$v.data.phoneNumber.minValue) {
        errors.push('Telefonnummer darf nur aus Zahlen bestehen.');
      }
      return errors;
    },
    participantRoleErrors() {
      const errors = [];
      if (!this.$v.data.participantRole.$dirty) return errors;
      if (!this.$v.data.participantRole.required) {
        errors.push('Es muss mindestens eine Fahrt ausgewählt werden.');
      }
      return errors;
    },
  },
  watch: {
    data() {
      if (this.$refs.zipCodeField) {
        this.$refs.zipCodeField.setValue(this.data.zipCode);
      }
      if (this.$refs.eatHabitType) {
        this.$refs.eatHabitType.setValue(this.data.eatHabitType);
      }
      if (this.$refs.eatHabitText) {
        this.$refs.eatHabitText.setValue(this.eatHabitText);
      }
    },
  },
  methods: {
    refresh() {},
    requiredField(value) {
      const errorMsg = 'Dieses Feld muss ausgefüllt werden.';
      if (value instanceof Array && value.length === 0) {
        return errorMsg;
      }
      return !!value || errorMsg;
    },
    validScoutGroup(value) {
      const errorMsg = 'Der Gruppenname muss mit Meute, Sippe oder Roverrunde beginnen';
      return !!scoutGroupStartValidator(value) || errorMsg;
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
        age: null,
        registration: null,
        eatHabitType: [],
        scoutGroup: null,
        isGroupLeader: false,
        roles: [],
      };
      this.eatHabitText = null;
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
      this.$refs.zipCodeField.$v.$reset();
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.$refs.zipCodeField.$v.$touch();
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
      if (this.eatHabitText) {
        this.data.eatHabitType.push(this.eatHabitText);
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
