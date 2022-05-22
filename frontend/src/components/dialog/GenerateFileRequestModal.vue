<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Datei anfodern</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row class="ma-4">
          Was für eine Datei willst du anfordern?
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
import { required } from 'vuelidate/lib/validators';

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
    open() {
      this.data = {};
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
      this.$emit('createFileRequest', this.data);
      this.active = false;
    },
  },
  validations: {
    data: {
      type: {
        required,
      },
      extension: {
        required,
      },
    },
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
            name: 'Model für Einzelanmeldungen auswählen',
            techName: 'type',
            tooltip: 'Wähle den Datei Typ aus.',
            icon: 'mdi-account-circle',
            lookupPath: '/event/choices/file-type/',
            lookupListDisplay: ['name'],
            mandatory: true,
            fieldType: 'enumCombo',
            default: '',
          },
          {
            name: 'Model für Einzelanmeldungen auswählen',
            techName: 'extension',
            tooltip: 'Wähle das Datei Format.',
            icon: 'mdi-account-circle',
            lookupPath: '/event/choices/file-extension/',
            lookupListDisplay: ['name'],
            mandatory: true,
            fieldType: 'enumCombo',
            default: '',
          },
        ],
      };
    },
  },
};
</script>
