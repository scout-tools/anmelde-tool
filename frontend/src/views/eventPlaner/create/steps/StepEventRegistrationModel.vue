<template>
  <v-form ref="StepEventRegistrationModel" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Bitte gib an wer sich wie registrieren kann.
            Können sich Stämme anmelden?
            Können sich Einzelpersonen anmelden?
            Müssen sich Stämme anmelden, bevor sich Einzelpersonen anmelden können?
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <p><b>Model für Einzelanmeldungen auswählen</b></p>
        <p>
          <br>No = No single person registrations allowed
          <br>Attached = A single persons'
          registration has to be attached to a group registration
          <br>Mixed = A single persons'
          registration can be attached to a group registration but is not a must
          <br>External = Only standalone single persons' registrations allowed
        </p>
      </v-row>
      <v-row align="center" justify="center">
        <p><b>Model für Gruppenanmeldungen auswählen</b></p>
        <p>
          <br>No = No group registration allowed
          <br>Optional = Group registration possible
          <br>Required = Group registration is required =>
          single registration can be only attached or not allowed at all
        </p>
      </v-row>
      <div v-for="(field, i) in fields" :key="i">
        <BaseField
          :field="field"
          v-model="data[field.techName]"
          :valdiationObj="$v"
        />
      </div>
      <prev-next-button
        :valid="valid"
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepEventRegistrationModel',
  header: 'Registrierungsmodel',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
    BaseField,
  },
  mixins: [stepMixin, apiCallsMixin, serviceMixin],
  data: () => ({
    valid: true,
    data: {},
    modulePath: '/event/event/',
    fields: [
      {
        name: 'Model für Einzelanmeldungen auswählen',
        techName: 'singleRegistration',
        tooltip: 'Wähle einen Registrierungsmodel für die Einzelanmeldungen aus.',
        icon: 'mdi-account-circle',
        lookupPath: '/event/event-type-single-choices/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'enumCombo',
        default: '',
      },
      {
        name: 'Model für Gruppenanmeldungen auswählen',
        techName: 'groupRegistration',
        tooltip: 'Wähle einen Registrierungsmodel für die Gruppenanmeldungen aus.',
        icon: 'mdi-account-circle',
        lookupPath: '/event/event-type-group-choices/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'enumCombo',
        default: '',
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
  }),
  validations: {
    data: {
      singleRegistration: {
        required,
      },
      groupRegistration: {
        required,
      },
      personalDataRequired: {
        required,
      },
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getService(this.id, this.modulePath);
    },
  },
  created() {
    this.loadData();
  },
};
</script>
