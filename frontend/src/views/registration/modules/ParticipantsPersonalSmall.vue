<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :loading="loading"
    :saving="saving"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
    @saving="onSaving"
  >
    <template v-slot:header>
      <p>
        Ich melde folgende Teilnehmende an <br/>
        <br/>
        Die Erfassung erfolgt pro Person. <br/>
        <br/>
        <v-icon color="red"> mdi-alert-circle</v-icon>
        Du musst dich selbst auch in die Liste eintragen.
      </p>
      <p v-if="!!dialogMeta.excelUpload">
        Alternativ kannst du hier die Excelliste hochladen, wenn du die Daten
        dort bereits erfasst hast.
        <br/>
        <a
          v-if="!!dialogMeta.excelUpload"
          target="_blank"
          :href="currentRegistration.cloudLink"
          style="color: blue"
        >
          Link zur Beispiel Excel Datei
        </a>
      </p>
    </template>

    <template v-slot:main>
      <ListWithDialogMain
        :ref="`dialog-main-${moduleId}`"
        :dialogMeta="dialogMeta"
        :valdiationObj="$v"
        @validate="validate"
      />
    </template>
  </GenericRegModul>
</template>

<script>
import {
  required,
  minLength,
  maxLength,
} from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';

export default {
  name: 'StepConsent',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'currentModule',
    'personalData',
  ],
  components: {
    GenericRegModul,
    ListWithDialogMain,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    loading: true,
    saving: false,
    moduleData: [],
    data: {},
  }),
  validations: {
    data: {
      firstName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      lastName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      scoutName: {
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      birthday: {
        required,
      },
      bookingOption: {
        required,
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    loadingRead: {
      get() {
        return !!this.loading;
      },
      set() {
      },
    },
    moduleId() {
      return this.currentModule.module.id;
    },
    myStamm() {
      return this.userinfo.stamm;
    },
    myBund() {
      return this.userinfo.bund;
    },
    eventName() {
      return this.currentEvent.name;
    },
    cloudLink() {
      return this.currentEvent.cloudLink;
    },
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: false,
        path: `event/registration/${this.currentRegistration.id}/single-participant`,
        listDisplay: ['firstName', 'lastName'],
        fields: [
          {
            name: 'Vorname*',
            techName: 'firstName',
            tooltip:
              'Vornamen eintragen. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Nachname*',
            techName: 'lastName',
            tooltip: 'Trage bitte den vollständigen Nachnamen ein.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Fahrtenname',
            techName: 'scoutName',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-campfire',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Geburtstag*',
            techName: 'birthday',
            tooltip: 'Trage bitte das Geburtsdatum des_der Teilnehmer_in ein.',
            icon: 'mdi-calendar',
            mandatory: true,
            fieldType: 'date',
            default: '',
          },
          {
            name: 'Geschlecht*',
            techName: 'gender',
            tooltip: 'Trage bitte das Geschlecht des_der Teilnehmer_in ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'weiblich',
                value: 'F',
              },
              {
                name: 'männlich',
                value: 'M',
              },
              {
                name: 'divers',
                value: 'D',
              },
              {
                name: 'Keine Angabe',
                value: 'N',
              },
            ],
          },
          {
            name: 'Essenbesonderheiten',
            techName: 'eatHabit',
            tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
            icon: 'mdi-food',
            mandatory: true,
            lookupPath: '/basic/eat-habits/',
            lookupListDisplay: ['name'],
            fieldType: 'refCombo',
            default: '',
          },
          {
            name: 'Buchungsoption',
            techName: 'bookingOption',
            tooltip: '123',
            icon: 'mdi-tent',
            mandatory: true,
            lookupPath: `/event/event/${this.currentEvent.id}/booking-options/`,
            lookupListDisplay: ['name', 'price', '$ €'],
            fieldType: 'refDropdown',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    validate(data) {
      this.data = data;
      this.$v.$touch();
    },
    beforeTabShow() {
      this.loadData();
      this.$refs[`dialog-main-${this.moduleId}`].beforeTabShow();
    },
    onNextStep() {
      this.saving = true;
      this.nextStep();
    },
    setDefaults() {
    },
    loadData() {
      this.saving = false;
      this.loading = true;
      Promise.all([this.getModule(this.moduleId, this.currentEvent.id)])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.loading = false;
          this.setDefaults();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
  },
};
</script>
