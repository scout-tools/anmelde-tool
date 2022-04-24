<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Du hast dich für eine Rechtemanagement mit Email Adressen entschieden!
            Jeder der Zugriff auf die Interna deines Events bekommen soll, muss hier mit seiner
            Email Adresse aufgeführt werden.
          <br/>
          <i>(Jede geschriebene E-Mail-Adresse muss mit Enter bestätigt werden!)</i>
        </span>
      </v-row>
      <v-row>
        <div v-for="(field, i) in fields" :key="i">
          <BaseField
            :field="field"
            v-model="data[field.techName]"
            :valdiationObj="$v"
          />
        </div>
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required, email } from 'vuelidate/lib/validators';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepEventAuthenticationInternal',
  header: 'DPV IDM',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    PrevNextButton,
    BaseField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    modulePath: 'event/event',
    data: {},
    fields: [
      {
        name: 'Kontaktdaten',
        techName: 'contacts',
        tooltip: 'Wähle die Keycloak Gruppe aus in der das Planungsteam ist. Falls die Gruppe fehlt bitte dem DPV bescheid geben.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'simpleCombo',
        default: '',
        cols: 12,
      },
    ],
  }),
  validations: {
    data: {
      contacts: {
        $each: {
          required,
          email,
        },
      },
    },
  },
  computed: {
    contactsErrors() {
      const errors = [];
      if (!this.$v.contacts.$dirty) return errors;
      if (!this.$v.contacts.required) {
        errors.push('Es muss mindestens eine Ansprechperson angegeben werden.');
      }
      if (this.$v.contacts.$each.$anyError) {
        errors.push('Es müssen gültige E-Mail-Adressen angegeben werden.');
      }
      return errors;
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getServiceById(this.modulePath, this.id).then((response) => {
        this.data.contacts = response.data.responsiblePersons;
        this.$forceUpdate();
      });
    },
  },
  created() {
    this.loadData();
  },
};
</script>
