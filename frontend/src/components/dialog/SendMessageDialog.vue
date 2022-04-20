<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Nachricht an das Anmelde-Tool Team</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
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
        <v-btn color="success" @click="onClickOkay"> Senden</v-btn>
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
  minLength,
  maxLength,
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
    data: {},
  }),
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    open() {
      this.active = true;
      this.data.createdBy = this.userinfo.preferred_username;
      this.data.createdByEmail = this.userinfo.email;
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.createServiceById('basic/message', this.data).then(() => {
        this.$root.globalSnackbar.show({
          message: 'Nachricht verschickt. Wir melden uns.',
          color: 'success',
        });
        this.active = false;
      });
    },
  },
  validations: {
    data: {
      createdBy: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(30),
      },
      createdByEmail: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(40),
        email,
      },
      messageType: {
        required,
      },
      messageBody: {
        required,
        minLength: minLength(10),
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
            name: 'Name',
            techName: 'createdBy',
            tooltip:
              'Vornamen eintragen. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Email',
            techName: 'createdByEmail',
            tooltip: 'Trage deine E-Mail Adresse an mit der wir dich kontaktieren sollen.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Nachrichtentyp*',
            techName: 'messageType',
            tooltip: 'Um welchen Nachrichtentyp handelt es sich.',
            icon: 'mdi-food',
            mandatory: true,
            lookupPath: '/basic/message-type/',
            lookupListDisplay: ['name'],
            multiple: false,
            fieldType: 'refComboSingle',
            default: '',
          },
          {
            name: 'Nachricht',
            techName: 'messageBody',
            tooltip: 'Was möchtest du uns mitteilen?',
            icon: 'mdi-message',
            mandatory: true,
            fieldType: 'textarea',
            default: '',
            cols: 12,
          },
        ],
      };
    },
  },
};
</script>

<style>
</style>
