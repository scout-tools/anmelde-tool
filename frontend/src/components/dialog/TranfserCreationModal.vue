<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="close">
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
  minLength, required,
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
    paymentData: {},
  }),
  methods: {
    validate() {
      this.$v.$touch();
      console.log(this.$v);
      this.valid = !this.$v.$anyError;
    },
    open(data, itemId) {
      this.paymentData = data;
      this.data = {};
      this.registrationId = itemId;
      this.active = true;
      this.setDefaults();
    },
    openEdit(data, itemId) {
      this.paymentData = data;
      this.registrationId = itemId;
      this.data = data;
      this.active = true;
      this.edit = true;
    },
    close() {
      this.active = false;
      this.registrationId = null;
      this.data = {};
      this.edit = false;
      this.$v.$reset();
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      const emit = this.edit ? 'editTransfer' : 'createTransfer';
      this.$emit(emit, this.data, this.registrationId);
      this.close();
    },
    setDefaults() {
      debugger;
      this.data.amount = this.openAmount;
      this.data.transferSubject = this.paymentData.refId;
      this.data.transferDate = new Date();
      this.data.transferPerson = this.paymentData.responsiblePersons[0].email;
    },
  },
  validations: {
    data: {
      transferSubject: {
        required,
        minLength: minLength(1),
      },
      transferDate: {
        required,
      },
    },
  },
  created() {
  },
  computed: {
    openAmount() {
      if (this.paymentData && this.paymentData.payement && this.paymentData.payement.open) {
        return this.paymentData.payement.open;
      }
      return '';
    },
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
            fieldType: 'date',
            cols: 6,
          },
          {
            name: 'Überweisende Person (Email-Adresse)',
            techName: 'transferPerson',
            icon: 'mdi-account-circle',
            lookupPath: '/auth/responsables/',
            lookupListDisplay: ['scoutName', '$ - ', 'stamm', '$ -', 'email', '$'],
            mandatory: false,
            fieldType: 'responsablesField',
            default: '',
            cols: 6,
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
            name: 'Persönliche Anmerkung',
            techName: 'description',
            tooltip: 'Hier kannst du persönliche Anmerkungen eintragen.',
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
