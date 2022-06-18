<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Veranstaltung Erstellung: Unveränderliche Daten</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row class="ma-4">
          Bitte fülle diese Daten aus, sie sind teilweise nicht mehr änderbar.
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
        <v-divider class="my-2" />
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
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import {
  required,
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
    data: {},
  }),
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    open() {
      this.active = true;
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('createEvent', this.data);
    },
  },
  validations: {
    data: {
      name: {
        required,
      },
      personalDataRequired: {
        required,
      },
      bookingOption: {
        required,
      },
      authName: {
        required,
      },
    },
  },
  created() {},
  computed: {
    ...mapGetters(['userinfo']),
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
            name: 'Veranstaltunganame (änderbar)',
            techName: 'name',
            tooltip: 'Wie ist der Lagername?',
            icon: 'mdi-account-circle',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Authentifierungsoption',
            techName: 'authName',
            tooltip:
              'Vornamen eintragen. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'DPV-Keycloak-Gruppen',
                value: 'KeycloakAuthorization',
              },
              {
                name: 'E-Mail Adressen',
                value: 'InternalAuthorization',
              },
            ],
          },
          {
            name: 'Buchungsart',
            techName: 'bookingOption',
            tooltip:
              'Vornamen eintragen. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'BookingOptionComplex',
                value: 'BookingOptionComplex',
              },
            ],
          },
          {
            name: 'Persönliche Daten erforderlich?',
            techName: 'personalDataRequired',
            tooltip: 'Möchtest du, dass persönliche Daten erfasst werden?',
            icon: 'mdi-account-circle',
            mandatory: true,
            fieldType: 'checkbox',
            default: '',
          },
        ],
      };
    },
  },
};
</script>

<style>
</style>
