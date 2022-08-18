<template>
  <v-container fluid class="pa-0">
    <div v-for="(field, i) in fields" :key="i">
      <BaseField
        :field="field"
        v-model="data[field.techName]"
        :valdiationObj="$v"
      />
    </div>
    <v-btn color="success" @click="createRegistration">Neue Anmeldung</v-btn>
  </v-container>
</template>

<script>
import BaseField from '@/components/common/BaseField.vue';
import axios from 'axios';

import {
  required,
} from 'vuelidate/lib/validators';

export default {
  components: {
    BaseField,
  },
  validations: {
    data: {
      stamm: {
        required,
      },
    },
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      regType: 'group',
    },
    fields: [
      {
        name: 'Organisation',
        techName: 'stamm',
        tooltip:
          'Welche Pfadfinder Organisation soll angemeldet werden?',
        icon: 'mdi-account-circle',
        lookupPath: '/basic/scout-hierarchy/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
      {
        name: 'Einzel/Gruppenanmeldung',
        techName: 'regType',
        tooltip:
          'Soll der Stamm oder eine einzelne Person angemeldet werden?',
        icon: 'mdi-home',
        mandatory: true,
        fieldType: 'radio',
        referenceDisplay: 'name',
        referenceTable: [
          {
            name: 'Einzelanmeldung',
            value: 'single',
          },
          {
            name: 'Gruppenanmeldung',
            value: 'group',
          },
        ],
      },
    ],
  }),
  methods: {
    createRegistration() {
      axios
        .post(`${this.API_URL}/event/registration/`, {
          eventCode: 'tt87',
          event: this.eventId,
          single: this.data.regType === 'single',
          scoutOrganisation: this.data.stamm,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationEdit',
            params: {
              id: response.data.id,
            },
          });
        })
        .catch((error) => {
          console.log(error);
          this.showError = true;
          this.errorMessage = error.response.data.detail;
        });
    },
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
};
</script>

<style>
</style>
