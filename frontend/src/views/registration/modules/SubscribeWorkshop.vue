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
            tooltip: '',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Gesamte Erlebnisangebot-Kosten',
            techName: 'currency',
            tooltip: '',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'number',
            default: '',
          },
          {
            name: 'min. Teilnehmende',
            techName: 'minPerson',
            tooltip: '',
            icon: 'mdi-counter',
            mandatory: true,
            fieldType: 'number',
            default: '',
          },
          {
            name: 'max. Teilnehmende*',
            techName: 'maxPerson',
            tooltip: '',
            icon: 'mdi-counter',
            mandatory: true,
            fieldType: 'date',
            default: '',
          },
          {
            name: 'Erlebnisangebot-Beschreibung',
            techName: 'freeText',
            tooltip: '',
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
