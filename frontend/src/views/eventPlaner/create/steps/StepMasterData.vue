<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row>
        <span class="text-left subtitle-1">
          Allgemeine Daten
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
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepMasterData',
  props: ['position', 'maxPos'],
  header: 'Stammdaten',
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
        name: 'Link zur Cloud',
        techName: 'cloudLink',
        tooltip: '123',
        icon: 'mdi-cloud',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Link zur Anmeldeseite',
        techName: 'event_url',
        tooltip: '123',
        icon: 'mdi-cloud',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Technischer Name',
        techName: 'technicalName',
        tooltip: '123',
        icon: 'mdi-robot',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Einladene Organisaion',
        techName: 'limitedRegistrationHierarchy',
        tooltip: '123',
        icon: 'mdi-account-circle',
        lookupPath: '/basic/scout-hierarchy/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      technicalName: {
        required,
      },
      limitedRegistrationHierarchy: {
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
