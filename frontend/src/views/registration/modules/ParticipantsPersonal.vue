<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="nextStep"
  >
    <template v-slot:header>
      <p>Döner</p>
    </template>

    <template v-slot:main>
      <ListWithDialogMain
        :ref="`dialog-main-${moduleId}`"
        :dialogMeta="dialogMeta"
      />
    </template>
  </GenericRegModul>
</template>

<script>
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
    isLoading: true,
    moduleData: [],
    data: {},
  }),
  validations: {
    data: {},
  },
  computed: {
    ...mapGetters(['userinfo']),
    isLoadingRead: {
      get() {
        return !!this.isloading;
      },
      set() {},
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
            name: 'Geburtstag',
            techName: 'birthday',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-calendar',
            mandatory: true,
            fieldType: 'date',
            default: '',
          },
          {
            name: 'E-Mail Adresse*',
            techName: 'birthday',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-email',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Geschlecht*',
            techName: 'gender',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'Frau',
                value: 'FEMALE',
              },
              {
                name: 'Mann',
                value: 'MALE',
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
              'Trage bitte den Wohnort oder die Postleitzahl des Wohnorts ein und wähle die richtige Option aus.',
            icon: 'mdi-city',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Telefonnummer*',
            techName: 'phoneNumber',
            tooltip:
              'Trage bitte eine Mobil- oder Festnetznummer ein unter der der_die Teilnehmer_in oder die Erziehungsberechtigten nach der Fahrt erreichbar sind.',
            icon: 'mdi-phone',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Buchungsoption',
            techName: 'bookingOption',
            tooltip: '123',
            icon: 'mdi-tent',
            mandatory: true,
            lookupPath: `/event/event/${this.currentEvent.id}/booking-options/`,
            lookupListDisplay: ['id', 'name'],
            fieldType: 'refDropdown',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
      this.$refs[`dialog-main-${this.moduleId}`].beforeTabShow();
    },
    setDefaults() {},
    loadData() {
      this.isLoading = true;
      Promise.all([this.getModule(this.moduleId)])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.isLoading = false;
          this.setDefaults();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
