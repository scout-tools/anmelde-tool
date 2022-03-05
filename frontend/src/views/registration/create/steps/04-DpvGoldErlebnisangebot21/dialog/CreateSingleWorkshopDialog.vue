<template>
  <v-dialog
    ref="workshopDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Erlebnisangebote hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-subheader class="ma-5">
          Ich melde folgendes Erlebnisangebot an.
        </v-subheader>
        <v-form v-model="valid">
          <v-divider />
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model.lazy="data.title"
                :counter="100"
                :error-messages="errorMessage('title')"
                label="Erlebnisangebot-Titel"
                required
                prepend-icon="mdi-card-account-details-outline"
                @input="$v.data.title.$touch()"
                @blur="$v.data.title.$touch()"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="info" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Trage bitte einen kurzen Namen für dein Erlebnisangebot ein.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>
          <v-divider />
          <v-row>
            <v-col cols="12" sm="6" md="4">
              <vuetify-money
                v-model="data.costs"
                :options="options"
                :properties="properties"
                :error-messages="errorMessage('costs')"
                label="Gesamte Erlebnisangebot-Kosten"
                @input="$v.data.costs.$touch()"
                @blur="$v.data.costs.$touch()"
              >
              </vuetify-money>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.minPerson"
                @input="$v.data.minPerson.$touch()"
                @blur="$v.data.minPerson.$touch()"
                :error-messages="errorMessage('minPerson')"
                number
                label="min. Teilnehmende"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="info" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Die minimale Anzahl an Teilnehmenden.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-text-field
                v-model="data.maxPerson"
                @input="$v.data.maxPerson.$touch()"
                @blur="$v.data.maxPerson.$touch()"
                :error-messages="errorMessage('maxPerson')"
                number
                label="max. Teilnehmende"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="info" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span>
                      {{
                        'Die maximale Anzahl an Teilnehmenden.'
                      }}
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" sm="6">
              <v-textarea
                filled
                v-model="data.freeText"
                :counter="1000"
                :error-messages="errorMessage('freeText')"
                label="Erlebnisangebot-Beschreibung"
                required
                prepend-icon="mdi-card-account-details-outline"
                @input="$v.data.freeText.$touch()"
                @blur="$v.data.freeText.$touch()"
              >
              </v-textarea>
            </v-col>
          </v-row>
          <v-divider class="my-3" />
          <v-btn color="secondary" @click="onClickOkay"> Speichern </v-btn>
        </v-form>
      </v-container>

      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Anlegen deines Erlebnisangebotes' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  required,
  minLength,
  maxLength,
  between,
  minValue,
  maxValue,
} from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  name: 'CreateSingleWorkshopDialog',
  props: ['isOpen'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    participants: [],
    isLoading: true,
    isEditWindow: false,
    menu: false,
    modal: false,
    menu2: false,
    data: {
      title: null,
      minPerson: 5,
      maxPerson: 10,
      freeText: null,
      costs: null,
      registration: null,
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
    options: {
      locale: 'de-DE',
      suffix: '€',
      precision: 2,
      max: 500.0,
    },
    properties: {
      'prepend-icon': 'mdi-cash',
    },
  }),
  validations: {
    data: {
      title: {
        required,
        minLength: minLength(3),
        maxLength: maxLength(100),
      },
      costs: {
        required,
        between: between(0.0, 500.0),
      },
      freeText: {
        required,
        minLength: minLength(3),
        maxLength: maxLength(1000),
      },
      minPerson: {
        required,
        minValue: minValue(3),
        maxValue: maxValue(100),
      },
      maxPerson: {
        required,
        minValue: minValue(4),
        maxValue: maxValue(100),
      },
    },
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'myStamm',
      'myBund',
    ]),
    email() {
      return this.getJwtData.email;
    },
  },
  methods: {
    getDisplayName(firstName, lastName, scoutName) {
      let returnString = `${firstName} ${lastName}`;
      if (scoutName) {
        returnString = `${returnString} (${scoutName})`;
      }
      return returnString;
    },
    errorMessage(field) {
      const errors = [];
      const valObj = this.$v.data[field];
      if (!valObj.$dirty) return errors;
      if (valObj.required === false) {
        errors.push('Dieses Feld ist erforderlich.');
      }
      if (valObj.minLength === false) {
        const { min } = valObj.$params.minLength;
        errors.push(`Du musst mindestens ${min} Zeichen nutzen.`);
      }
      if (valObj.maxLength === false) {
        const { max } = valObj.$params.maxLength;
        errors.push(`Du darfst maximal ${max} Zeichen nutzen.`);
      }
      if (valObj.minValue === false) {
        errors.push(`Minimal sind ${valObj.$params.minValue.min} erlaubt.`);
      }
      if (valObj.maxValue === false) {
        errors.push(`Maximal sind ${valObj.$params.maxValue.max} erlaubt.`);
      }
      if (valObj.between === false) {
        const { min, max } = valObj.$params.between;
        errors.push(`Bitte gib einen Wert zwischen ${min}€ und ${max}€ ein. Falls du mehr als ${max}€ brauchst melde dich bei der Lagerleitung.`);
      }
      return errors;
    },
    onClickOk() {
      this.active = false;
    },
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.data = {
        title: null,
        freeText: null,
        costs: null,
        minPerson: null,
        maxPerson: null,
        registration: null,
      };
      this.isEditWindow = false;
      this.active = true;
      this.loadData();
    },
    openDialogEdit(input) {
      this.data = input;
      this.isEditWindow = true;
      this.active = true;
      this.loadData();
    },
    loadData() {
      this.isLoading = true;

      Promise.all([this.loadParticipants()])
        .then((values) => {
          [this.participants] = values;
          this.participants = this.participants[0].participantpersonalSet.map(
            // eslint-disable-next-line
            ({ firstName, lastName, scoutName, ...args }) => ({
              name: this.getDisplayName(firstName, lastName, scoutName),
              ...args,
            }),
          );
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadParticipants() {
      const path = `${this.API_URL}basic/registration/${
        this.$route.params.id
      }/participants/?&timestamp=${new Date().getTime()}`;
      const response = await axios.get(path);
      return response.data;
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

      if (!this.data.id) {
        axios.post(`${this.API_URL}basic/workshop/`, this.data).then(() => {
          this.closeDialog();
          this.$emit('refresh');
        });
      } else {
        axios
          .put(`${this.API_URL}basic/workshop/${this.data.id}/`, this.data)
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
