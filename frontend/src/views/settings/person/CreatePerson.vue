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
        <v-toolbar-title>Eintrag</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container v-if="!isLoading">
        <v-row>
          <template v-for="(field, i) in dialogMeta.fields">
            <BaseField
              :key="i"
              :field="field"
              v-model="data[field.techName]"
              :valdiationObj="$v"
            />
          </template>
        </v-row>
        <v-divider class="my-3" />
        <v-btn color="success" @click="onClickOkay"> Speichern</v-btn>
      </v-container>
      <v-container v-else>
        <Circual />
      </v-container>
      <v-divider class="my-4" />
      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Hochladen' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';
import Circual from '@/components/loading/Circual.vue';

import {
  required,
  minLength,
  maxLength,
  email,
} from 'vuelidate/lib/validators';

export default {
  components: {
    BaseField,
    Circual,
  },
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {},
    showError: false,
    showSuccess: false,
    timeout: 7000,
    isLoading: true,
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
      scoutName: {
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      email: {
        email,
      },
      birthday: {
        required,
        minYearAge(val) {
          const date = new Date(new Date().getFullYear() - 100, 0, 1);
          return new Date(val) > date;
        },
      },
      gender: {
        required,
      },
      address: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(40),
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
    },
  },
  computed: {
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: true,
        path: 'auth/person',
        listDisplay: ['firstName', 'lastName'],
        orderBy: 'firstName',
        maxItems: null,
        minItems: 1,
        fields: [
          {
            name: 'Vorname*',
            techName: 'firstName',
            tooltip:
              'Vornamen eintragen. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Nachname*',
            techName: 'lastName',
            tooltip: 'Trage bitte den vollständigen Nachnamen ein.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Fahrtenname',
            techName: 'scoutName',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-campfire',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Geburtstag*',
            techName: 'birthday',
            tooltip: 'Trage bitte das Geburtsdatum des_der Teilnehmer_in ein.',
            icon: 'mdi-calendar',
            mandatory: true,
            fieldType: 'date',
            default: '',
          },
          {
            name: 'E-Mail Adresse',
            techName: 'email',
            tooltip:
              'Trage bitte die E-Mail Adresse des_der Teilnehmer_in ein.',
            icon: 'mdi-email',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Geschlecht*',
            techName: 'gender',
            tooltip: 'Trage bitte das Geschlecht des_der Teilnehmer_in ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'weiblich',
                value: 'F',
              },
              {
                name: 'männlich',
                value: 'M',
              },
              {
                name: 'divers',
                value: 'D',
              },
              {
                name: 'Keine Angabe',
                value: 'N',
              },
            ],
          },
          {
            name: 'Straße und Hausnummer*',
            techName: 'address',
            tooltip: 'Trage bitte Straße und Hausnummer ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Postleitzahl/Ort*',
            techName: 'zipCode',
            tooltip:
              'Trage bitte den Wohnort oder die Postleitzahl des Wohnortes aus.',
            icon: 'mdi-city',
            mandatory: true,
            fieldType: 'zipField',
            default: '',
            lookupListDisplay: ['zipCode', 'city'],
          },
          {
            name: 'Telefonnummer',
            techName: 'phoneNumber',
            tooltip:
              'Trage bitte eine Mobil- oder Festnetznummer ein unter der der_die Teilnehmer_in oder die Erziehungsberechtigten nach der Fahrt erreichbar sind.',
            icon: 'mdi-phone',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Essenbesonderheiten',
            techName: 'eatHabits',
            tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
            icon: 'mdi-food',
            mandatory: true,
            lookupPath: '/basic/eat-habits/',
            lookupListDisplay: ['name'],
            fieldType: 'refCombo',
            default: '',
          },
          {
            name: 'Position*',
            techName: 'leader',
            tooltip:
              'Wenn die Person eine Führungsposition ausführt, bitte angeben',
            icon: 'mdi-office-building ',
            mandatory: false,
            lookupPath: '/event/choices/leader-types/',
            lookupListDisplay: ['name'],
            fieldType: 'enumCombo',
            multiple: false,
            default: 'N',
          },
        ],
      };
    },
  },
  methods: {
    openDialog(item) {
      this.active = true;
      this.isEditWindow = false;
      if (item) {
        this.data = item;
      } else {
        this.setDefaults();
      }
      this.$forceUpdate();
      this.isLoading = false;
    },
    openDialogEdit(item) {
      this.active = true;
      this.isEditWindow = true;
      if (item.id) {
        this.data.id = item.id;
        this.getData(item.id);
      } else {
        this.setDefaults();
      }
    },
    setDefaults() {
      this.data = {};
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
      this.$forceUpdate();
      this.validate();
      if (this.valid) {
        try {
          this.callCreateService();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    getData(id) {
      this.isLoading = true;
      this.getServiceById(this.dialogMeta.path, id)
        .then((response) => {
          this.data = response.data;
        })
        .catch((error) => {
          this.$root.globalSnackbar.show({
            message: error.response.data,
            color: 'error',
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    async callCreateService() {
      this.isLoading = true;
      if (!this.isEditWindow) {
        this.createServiceById(this.dialogMeta.path, this.data)
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
            this.$root.globalSnackbar.show({
              message: 'Neuer Eintrag angelegt',
              color: 'success',
            });
          })
          .catch((error) => {
            let errorMessage = 'Es ist ein Fehler beim speichern aufgetreten.';
            const errorData = error.response.data;
            try {
              const errorMessages = [];
              const keys = Object.keys(errorData);
              keys.forEach((key) => {
                errorMessages.push(`Fehler bei ${key}: ${errorData[key]}`);
              });
              errorMessage = errorMessages.join(' - ');
            } catch {
              console.log('Fehler');
            }
            this.$root.globalSnackbar.show({
              message: errorMessage,
              color: 'error',
            });
          });
      } else {
        this.updateServiceById(this.dialogMeta.path, this.data)
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          })
          .catch((error) => {
            let errorData = error.response;
            if (error.response.data.detail) {
              errorData = error.response.data.detail;
            }
            this.$root.globalSnackbar.show({
              message: errorData,
              color: 'error',
            });
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },
  },
};
</script>
