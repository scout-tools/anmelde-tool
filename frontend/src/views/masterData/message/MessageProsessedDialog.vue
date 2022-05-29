<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Nachricht bearbeiten</v-toolbar-title>
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
        <v-divider class="my-2" />
        <v-row class="ma-1">
                  <v-spacer></v-spacer>
        <v-btn color="success" @click="onClickOkay">Speichern</v-btn>
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
    open(item) {
      this.data = item;
      this.active = true;
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.updateMessageById(this.data).then(() => {
        this.$emit('refresh');
        this.active = false;
      });
    },
  },
  validations: {
    data: {
      messageType: {
        required,
      },
      isProcessed: {
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
            name: 'Typ',
            techName: 'messageType',
            tooltip: 'Welcher Typ?',
            icon: 'mdi-shape',
            lookupPath: '/basic/message-type/',
            lookupListDisplay: ['name'],
            mandatory: true,
            fieldType: 'refDropdown',
            default: '',
          },
          {
            name: 'Personen',
            techName: 'supervisor',
            tooltip: 'Welcher Typ?',
            icon: 'mdi-shape',
            lookupPath: '/auth/responsables/',
            lookupListDisplay: ['scoutName', '$ - ', 'stamm', '$ -', 'email', '$'],
            mandatory: true,
            fieldType: 'responsablesField',
            default: '',
          },
          {
            name: 'Bearbeitet?',
            techName: 'isProcessed',
            tooltip: 'Is der Fall erledigt?',
            icon: 'mdi-account-circle',
            mandatory: true,
            fieldType: 'checkbox',
            default: '',
          },
          {
            name: 'Interner Vermerk',
            techName: 'internalComment',
            tooltip: 'Interner Vermerk?',
            icon: 'mdi-account-circle',
            mandatory: true,
            fieldType: 'textarea',
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
