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
          v-if="dialogMeta.excelUpload"
          target="_blank"
          :href="cloudLink"
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
        :currentEvent="currentEvent"
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
  email,
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
      email: {
        email,
      },
      birthday: {
        required,
        minYearAge(val) {
          const date = new Date(new Date().getFullYear() - 100, 0, 1);
          return new Date(val) > date;
        },
      },
      gender: {
        required,
      },
      bookingOption: {
        required,
      },
      street: {
        required,
        minLength: minLength(4),
        maxLength: maxLength(40),
      },
      zipCode: {
        required,
        minLength: minLength(1),
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
        excelUpload: true,
        path: `event/registration/${this.currentRegistration.id}/single-participant`,
        listDisplay: ['firstName', 'lastName'],
        orderBy: 'firstName',
        maxItems: null,
        minItems: 1,
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
            name: 'E-Mail Adresse',
            techName: 'email',
            tooltip:
              'Trage bitte die E-Mail Adresse des_der Teilnehmer_in ein.',
            icon: 'mdi-email',
            mandatory: true,
            fieldType: 'textfield',
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
            name: 'Straße und Hausnummer*',
            techName: 'street',
            tooltip: 'Trage bitte Straße und Hausnummer ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Postleitzahl/Ort*',
            techName: 'zipCode',
            tooltip:
              'Trage bitte den Wohnort oder die Postleitzahl des Wohnortes aus.',
            icon: 'mdi-city',
            mandatory: true,
            fieldType: 'zipField',
            default: '',
            lookupListDisplay: ['zipCode', 'city'],
          },
          {
            name: 'Telefonnummer',
            techName: 'phoneNumber',
            tooltip:
              'Trage bitte eine Mobil- oder Festnetznummer ein unter der der_die Teilnehmer_in oder die Erziehungsberechtigten nach der Fahrt erreichbar sind.',
            icon: 'mdi-phone',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
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
            name: 'Position*',
            techName: 'leader',
            tooltip:
              'Wenn die Person eine Führungsposition ausführt, bitte angeben',
            icon: 'mdi-office-building ',
            mandatory: false,
            lookupPath: '/event/choices/leader-types/',
            lookupListDisplay: ['name'],
            fieldType: 'enumCombo',
            multiple: false,
            default: 'N',
          },
          {
            name: 'Buchungsoption*',
            techName: 'bookingOption',
            tooltip: 'Wie möchte diese Person an der Veranstaltung teilnehmen?',
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
