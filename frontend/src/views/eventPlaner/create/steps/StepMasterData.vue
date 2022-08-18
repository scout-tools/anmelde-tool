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
import { required, helpers, url } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

const alphaNumExtendedValidator = helpers.regex('alphaNumAndHyphen', /^[a-z\d-]*$/);

export default {
  name: 'StepMasterData',
  props: [
    'position',
    'maxPos',
    'event',
  ],
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
        tooltip: 'Link zu einem Cloud Ordner mit allen Dokumenten für die Teilnehmer.',
        icon: 'mdi-cloud',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Link zur Anmeldeseite',
        techName: 'eventUrl',
        tooltip: 'Link zur Aktionshomepage.',
        icon: 'mdi-cloud',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Technischer Name',
        techName: 'technicalName',
        tooltip: 'Dieser Name wird z.B. als Absender für E-Mails verwendet. Er darf keine Sonderzeichen enthallten.',
        icon: 'mdi-robot',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Einladene Organisation',
        techName: 'limitedRegistrationHierarchy',
        tooltip: 'Welche Pfadfinder Organisation lädt ein? Nur die Stämme unterhalb der Organisation können das Event sehen.',
        icon: 'mdi-account-circle',
        lookupPath: '/basic/scout-hierarchy/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
      {
        name: 'Lager-Icon',
        techName: 'icon',
        tooltip: 'Welche Logo soll auf der Startseite erscheinen?',
        icon: 'mdi-penguin',
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Theme',
        techName: 'theme',
        tooltip: 'Das Farbschema für dein Event',
        icon: 'mdi-palette',
        lookupPath: '/basic/theme/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      cloudLink: {
        url,
      },
      eventUrl: {
        url,
      },
      technicalName: {
        required,
        alphaNumExtendedValidator,
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
      this.getDataService(this.id, this.modulePath);
    },
  },
  // created() {
  //   this.loadData();
  // },
};
</script>
