<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Überweisung eintragen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row class="ma-4">
          Bitte fülle diese Daten aus.
        </v-row>
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
        <v-divider class="my-2"/>
        <v-row class="ma-1">
          <v-spacer></v-spacer>
          <v-btn color="success" @click="onClickOkay"> Speichern und weiter</v-btn>
        </v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import BaseField from '@/components/common/BaseField.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import {
  required,
  numeric,
  minLength,
  email,
} from 'vuelidate/lib/validators';

export default {
  components: {
    BaseField,
  },
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    edit: false,
    data: {},
    registrationId: '',
  }),
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    open(itemId) {
      this.data = {};
      this.registrationId = itemId;
      this.active = true;
    },
    openEdit(data) {
      this.registrationId = data.registration;
      this.data = data;
      this.active = true;
      this.edit = true;
    },
    close() {
      this.active = false;
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      const emit = this.edit ? 'editTransfer' : 'createTransfer';
      this.$emit(emit, this.data, this.registrationId);
      this.active = false;
    },
  },
  validations: {
    data: {
      amount: {
        required,
        numeric,
      },
      transferSubject: {
        required,
        minLength: minLength(1),
      },
      transferDate: {
        required,
      },
      transferPerson: {
        email,
      },
    },
  },
  created() {
  },
  computed: {
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: true,
        listDisplay: ['firstName', 'lastName'],
        orderBy: 'firstName',
        maxItems: null,
        minItems: 1,
        fields: [
          {
            name: 'Betrag*',
            techName: 'amount',
            tooltip: 'Wieviel wurde überwiesen?',
            icon: 'mdi-cash',
            mandatory: true,
            fieldType: 'currency',
            default: '',
            cols: 4,
          },
          {
            name: 'Verwendungszweck*',
            techName: 'transferSubject',
            tooltip:
              'Wie lautet der Verwendungszweck der Überweisung?'
              + ' (damit man diese später leichter wieder erkennen kann).',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'textfield',
            cols: 8,
          },
          {
            name: 'Überweisungsdatum*',
            techName: 'transferDate',
            tooltip:
              'Wann wurde die Überweisung getätigt?',
            icon: 'mdi-calendar-range',
            mandatory: true,
            fieldType: 'datetime',
            cols: 12,
          },
          {
            name: 'Überweisende Person (Email-Adresse)',
            techName: 'transferPerson',
            icon: 'mdi-account-circle',
            lookupPath: '/auth/responsables/',
            lookupListDisplay: ['scoutName', '$ - ', 'stamm', '$ -', 'email', '$'],
            mandatory: true,
            fieldType: 'responsablesField',
            default: '',
            cols: 12,
          },
          {
            name: 'Referenz Id',
            techName: 'transferReferenceId',
            tooltip: 'Gibt es eine Referenz Id?'
              + ' (damit man diese später leichter wieder erkennen kann).',
            icon: 'mdi-account-circle',
            mandatory: false,
            fieldType: 'textfield',
            cols: 6,
          },
          {
            name: 'Persöhnliche Anmerkung',
            techName: 'description',
            tooltip: 'Hier kannst du persöhnliche Anmerkungen eintragen.',
            icon: 'mdi-semantic-web',
            mandatory: false,
            fieldType: 'textarea',
            cols: 6,
          },
        ],
      };
    },
  },
};
</script>
