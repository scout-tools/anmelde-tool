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
          Ich melde folgende_n Teilnehmer_in an.
        </v-subheader>
        <v-form v-model="valid">
          <v-divider />
          <v-subheader> Namen </v-subheader>
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
                      {{
                        'Trage bitte den Vornamen des_der Teilnehmer_in ' +
                        'ein. Zweitnamen müssen nicht mit angegeben werden.'
                      }}
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
                      {{ 'Trage bitte den vollständigen Nachnamen ein.' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.scoutName"
                autofocus
                :counter="20"
                :error-messages="scoutNameErrors"
                label="Fahrtenname (optional)"
                required
                prepend-icon="mdi-campfire"
                @input="$v.data.scoutName.$touch()"
                @blur="$v.data.scoutName.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Trage bitte den Fahrtennamen ' +
                        'des_der Teilnehmer_in ein.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                transition="scale-transition"
                offset-y
                min-width="auto"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    v-model="computedDateFormattedMomentjs"
                    label="Geburtstag"
                    prepend-icon="mdi-calendar"
                    :error-messages="birthdayErrors"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                  v-model="data.birthday"
                  :active-picker.sync="activePicker"
                  :max="
                    new Date(
                      new Date('2021-12-24T03:24:00') -
                        new Date().getTimezoneOffset() * 60000,
                    )
                      .toISOString()
                      .substr(0, 10)
                  "
                  min="1950-01-01"
                  @change="save"
                ></v-date-picker>
              </v-menu>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="data.ageGroup"
                :items="ageGroupMapping"
                :error-messages="ageGroupsErrors"
                item-text="name"
                prepend-icon="mdi-account-group"
                item-value="id"
                label="Stufe"
                required
                @input="validate()"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.email"
                label="E-Mail Adresse*"
                prepend-icon="mdi-email"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{ tooltip.email }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>

          <v-divider />
          <v-subheader> Adresse / Telefon </v-subheader>
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.street"
                :counter="40"
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
                      {{ 'Trage bitte Straße und Hausnummer ein.' }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="data.zipCode"
                :items="zipCodeResponse"
                :item-text="customText"
                required
                :error-messages="zipCodeErrors"
                item-value="id"
                label="Stadt / Postleitzahl"
                placeholder="Wähle Stadt oder Postleitzahl."
                prepend-icon="mdi-city"
                :loading="isZipLoading"
                :search-input.sync="search"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Trage bitte den Wohnort oder die Postleitzahl ' +
                        'des Wohnorts ein und wähle die richtige Option aus.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.phoneNumber"
                :counter="30"
                :error-messages="phoneNumberErrors"
                label="Telefonnummer"
                prepend-icon="mdi-phone"
                required
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Trage bitte eine Mobil- oder Festnetznummer ' +
                        'ein unter der der_die Teilnehmer_in oder die ' +
                        'Erziehungsberechtigten nach ' +
                        'der Fahrt erreichbar sind.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
          <v-divider />
          <v-subheader> Tagesgast </v-subheader>
          <v-row>
            <v-col cols="12" sm="6">
              <v-container fluid>
                <v-switch v-model="isDayGuest" label="Tagesgast am Samstag">
                  <template slot="append">
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-icon color="success" dark v-bind="attrs" v-on="on">
                          mdi-help-circle-outline
                        </v-icon>
                      </template>
                      <span>
                        {{ 'Tagesgast?' }}
                      </span>
                    </v-tooltip>
                  </template>
                </v-switch>
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
  required,
  minLength,
  maxLength,
  integer,
  minValue,
} from 'vuelidate/lib/validators';
import axios from 'axios';
import moment from 'moment';
import { mapGetters } from 'vuex';

const scoutGroupStartValidator = (groupObjOrGroupName) => {
  const validStarts = ['Meute', 'Sippe', 'Roverrunde'];
  if (!groupObjOrGroupName) {
    return false;
  }
  const name = groupObjOrGroupName.name
    ? groupObjOrGroupName.name
    : groupObjOrGroupName;
  return validStarts.includes(name.trim().split(' ')[0]);
};

const eatHabitStartValidator = (habit) => {
  if (!habit) {
    return false;
  }
  let oneFalse = 0;
  habit.forEach((h) => {
    if (!h.startsWith('Kein')) oneFalse += 1;
    return oneFalse;
  });
  return oneFalse === 0;
};

const phoneNumStartValidator = (number) => {
  if (!number) return false;
  console.log(number);
  return number.startsWith('0');
};

export default {
  props: ['isOpen'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    scoutHierarchyGroups: [],
    eatHabitTypeMapping: [],
    isLoading: true,
    isEditWindow: false,
    eatHabitText: [],
    isDayGuest: false,
    isZipLoading: false,
    zipCodeResponse: [],
    activePicker: null,
    search: null,
    menu: false,
    modal: false,
    menu2: false,
    data: {
      firstName: null,
      lastName: null,
      street: null,
      zipCode: null,
      phoneNumber: null,
      birthday: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      ageGroup: null,
      registration: null,
      eatHabitType: [],
      scoutGroup: 'Test',
      isGroupLeader: false,
      participantRole: 5,
    },
    tooltip: {
      scoutName: 'Gib hier bitte deinen Namen oder deinen Fahrtennamen ein.',
      email:
        'Die E-Mail nutzen wir für die Kommunikation mit dem Tool und für Rückfragen.',
      mobileNumber:
        'Die Handynummer ist freiwillig und hilft dich zu kontaktieren (Für manche Fahrten ist sie Pflicht)',
      scoutOrganisation: 'Mit dem Stift kannst du deinen Stamm auswählen.',
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  watch: {
    menu(val) {
      val && this.$nextTick(() => { // eslint-disable-line
        this.activePicker = 'YEAR'; // eslint-disable-line
      });
    },
    search(searchString) {
      // still loading
      if (this.isZipLoading) return;

      if (!searchString) return;

      if (searchString.indexOf(' ') >= 0) return;

      if (searchString && searchString.length <= 1) return;

      this.isZipLoading = true;

      this.getZipCodeMapping(searchString)
        .then((res) => {
          this.zipCodeResponse = res;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.isZipLoading = false;
        });
    },
  },
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
      scoutName: {
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      ageGroup: {
        required,
      },
      phoneNumber: {
        required,
        integer,
        minValue: minValue(1),
        phoneNumStartValidator,
      },
      birthday: {
        required,
      },
      street: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(30),
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
    },
    eatHabitText: {
      eatHabitStartValidator,
    },
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'ageGroupMapping',
    ]),
    computedDateFormattedMomentjs() {
      return this.data.birthday ? moment(this.data.birthday).format('DD.MM.YYYY') : '';
    },
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
    ageGroupsErrors() {
      const errors = [];
      if (!this.$v.data.ageGroup.$dirty) return errors;
      if (!this.$v.data.ageGroup.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
    birthdayErrors() {
      const errors = [];
      if (!this.$v.data.birthday.$dirty) return errors;
      if (!this.$v.data.birthday.required) {
        errors.push('Alter ist erforderlich.');
      }
      return errors;
    },
    phoneNumberErrors() {
      const errors = [];
      if (!this.$v.data.phoneNumber.$dirty) return errors;
      if (!this.$v.data.phoneNumber.required) {
        errors.push('Telefonnummer ist erforderlich.');
      }
      if (
        !this.$v.data.phoneNumber.integer || // eslint-disable-line
        !this.$v.data.phoneNumber.minValue // eslint-disable-line
      ) {
        errors.push('Telefonnummer darf nur aus Zahlen bestehen.'); // eslint-disable-line
      }
      if (!this.$v.data.phoneNumber.phoneNumStartValidator) {
        errors.push('Die Telefonnummer muss mit 0 beginnen.');
      }
      return errors;
    },
    scoutNameErrors() {
      const errors = [];
      if (!this.$v.data.scoutName.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.data.scoutName.maxLength &&
        errors.push('Darf nicht mehr als 20 Zeichen haben');
      return errors;
    },
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.data.zipCode.$dirty) return errors;

      if (!this.$v.data.zipCode.minLength) {
        errors.push('Stadt ist erforderlich.');
      }

      if (!this.$v.data.zipCode.required) {
        errors.push('Stadt ist erforderlich.');
      }
      return errors;
    },
    eatHabitTypeErrors() {
      const errors = [];
      if (!this.$v.eatHabitText.eatHabitStartValidator) {
        errors.push('Die Essensgewohnheiten müssen mit Kein(e/r) starten.');
      }
      return errors;
    },
  },
  methods: {
    async getZipCodeMapping(searchString) {
      const path = `${this.API_URL}basic/zip-code/?zip_city=${searchString}`;
      const response = await axios.get(path);

      return response.data;
    },
    async callSingleZipCode(id) {
      const path = `${this.API_URL}basic/zip-code/?id=${id}`;
      const response = await axios.get(path);

      return response.data;
    },
    save(date) {
      this.$refs.menu.save(date);
    },
    customText: (item) => `${item.zipCode} — ${item.city}`,
    requiredField(value) {
      const errorMsg = 'Dieses Feld muss ausgefüllt werden.';
      if (value instanceof Array && value.length === 0) {
        return errorMsg;
      }
      return !!value || errorMsg;
    },
    validScoutGroup(value) {
      const errorMsg = // eslint-disable-line
        'Der Gruppenname muss mit Meute, Sippe oder Roverrunde beginnen'; // eslint-disable-line
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
        scoutName: null,
        street: null,
        zipCode: null,
        phoneNumber: null,
        age: null,
        registration: null,
        eatHabitType: [],
        scoutGroup: 'Test',
        isGroupLeader: false,
        roles: [],
        participantRole: 1,
        email: '',
        birthday: '',
      };
      this.eatHabitText = [];
      this.isDayGuest = false;
      this.isEditWindow = false;
      this.active = true;
      this.loadData();
    },
    openDialogEdit(input) {
      this.data = input;
      this.active = true;
      this.isEditWindow = true;

      this.getSingleZipCode(this.data.zipCode);
      this.loadData();
    },
    getSingleZipCode(zipCode) {
      this.callSingleZipCode(zipCode)
        .then((res) => {
          this.zipCodeResponse = res;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.isZipLoading = false;
        });
    },
    loadData() {
      this.isDayGuest = this.data.participantRole === 11;
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
      console.log(this.$v);
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
      this.data.participantRole = this.isDayGuest ? 11 : 1;
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
