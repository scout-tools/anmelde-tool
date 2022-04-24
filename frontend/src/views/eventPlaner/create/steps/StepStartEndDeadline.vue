<template>
  <v-form ref="forStartEndDeadline" v-model="valid">
    <v-container>
      <v-row class="my-6">
        <span class="subtitle-1"> Zeitraum der Aktion. </span>
      </v-row>
      <v-row>
        <template v-for="(field, i) in fields">
          <BaseField
            :key="i"
            :field="field"
            v-model="data[field.techName]"
            :valdiationObj="$v"
          />
        </template>
      </v-row>
      <v-divider class="my-2" />
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
  name: 'StepNameDescription',
  header: 'Daten und Uhrzeit',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  components: {
    PrevNextButton,
    BaseField,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      valid: true,
      data: {},
      modulePath: '/event/event/',
      fields: [
        {
          name: 'Start',
          techName: 'startDate',
          tooltip: 'Wann bedinngt deine Veranstaltung?',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Ende',
          techName: 'endDate',
          tooltip: 'Wann endet deine Veranstaltung?',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Anmeldestart',
          techName: 'registrationStart',
          tooltip: 'Ab wann dürfen sich deine Teilnehmer anmelden?',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Anmeldeende',
          techName: 'registrationDeadline',
          tooltip: 'Was ist der letzte Tag an dem die Anmeldung möglich ist?',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Letze Änderung',
          techName: 'lastPossibleUpdate',
          tooltip: 'Bis wann dürfen Änderungen an der Anmeldung vorgenommen werden?',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
      ],
    };
  },
  mixins: [stepMixin, apiCallsMixin, serviceMixin],
  validations: {
    data: {
      startDate: {
        required,
      },
      endDate: {
        required,
      },
      registrationStart: {
        required,
      },
      registrationDeadline: {
        required,
      },
      lastPossibleUpdate: {
        required,
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
  created() {
    this.loadData();
  },
};
</script>
