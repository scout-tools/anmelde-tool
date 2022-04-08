<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :loading="loading"
    :saving="saving"
    :position="position"
    :maxPos="maxPos"
    :currentMod="currentModule"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
    @saving="onSaving"
  >
    <template v-slot:header>
      <p>
        Bitte trage hier dein Erlebnisangebot ein. <br />
        <br />
        Falls du Inspirationen oder Ideen brauchst kannst du gerne
        <a
          style="color: blue"
          target="_blank"
          href="https://docs.google.com/document/d/1DoACKvb5GdbcfumOU1vLRAM_JXjA_bcdKblyuxDGCwA/edit?usp=sharing"
          >hier</a
        >
        schauen.
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
    showError: false,
    errorMessage: 'Fehler',
    data: {},
  }),
  validations: {
    data: {
      title: {
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
        path: `event/registration/${this.currentRegistration.id}/workshop`,
        listDisplay: ['title'],
        fields: [
          {
            name: 'Erlebnisangebot-Titel',
            techName: 'title',
            tooltip: 'Trage bitte einen kurzen Namen für dein Erlebnisangebot ein.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Gesamte Erlebnisangebot-Kosten',
            techName: 'currency',
            tooltip: 'Trage die maximalen Gesamtkosten hier ein.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'number',
            default: '',
          },
          {
            name: 'min. Teilnehmende',
            techName: 'minPerson',
            tooltip: 'Die minimale Anzahl an Teilnehmenden',
            icon: 'mdi-counter',
            mandatory: true,
            fieldType: 'number',
            default: '',
          },
          {
            name: 'max. Teilnehmende*',
            techName: 'maxPerson',
            tooltip: 'Die maximale Anzahl an Teilnehmenden.',
            icon: 'mdi-counter',
            mandatory: true,
            fieldType: 'date',
            default: '',
          },
          {
            name: 'Erlebnisangebot-Beschreibung',
            techName: 'freeText',
            tooltip: 'Beschreibe dein Erlebnisangebot möglichst genau.',
            icon: 'mdi-text',
            mandatory: true,
            fieldType: 'textarea',
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
