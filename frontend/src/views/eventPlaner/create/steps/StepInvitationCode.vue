<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row>
        <span class="text-left subtitle-1">
          Lege für die Aktion einen 6-Stelligen Verifizierungscode fest. <br />
          Dieser besteht aus Buchstaben und Zahlen und wird bei der Anmeldung
          mitgeschickt, damit sich die Anmelder verifizieren können, dass sie
          eingeladen wurden. <br />
          Bei leerem Feld gibt es keinen Verifizierungscode.
        </span>
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
import { required, maxLength, minLength } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepInvitationCode',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  header: 'Verifizierungscode',
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
        name: 'Verifizierungscode (Universell)',
        techName: 'invitationCode',
        tooltip: 'Dieser Code gilt für Einzel und Gruppenanmeldungen.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
        cols: 12,
      },
      {
        name: 'Verifizierungscode (Gruppenanmeldung)',
        techName: 'invitationCodeGroup',
        tooltip: 'Dieser Code gilt nur für Gruppenanmeldungen.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
        cols: 12,
      },
      {
        name: 'Verifizierungscode (Einzelanmeldung)',
        techName: 'invitationCodeSingle',
        tooltip: 'Dieser Code gilt nur für Einzelanmeldungen.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
        cols: 12,
      },
    ],
  }),
  validations: {
    data: {
      invitationCode: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(12),
      },
      invitationCodeGroup: {
        minLength: minLength(4),
        maxLength: maxLength(12),
      },
      invitationCodeSingle: {
        minLength: minLength(4),
        maxLength: maxLength(12),
      },
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getDataService(this.id, this.modulePath);
    },
  },
  // created() {
  //   this.loadData();
  // },
};
</script>
