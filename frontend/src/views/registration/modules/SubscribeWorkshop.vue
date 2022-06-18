<template>
  <v-container>
    <v-container v-if="!loading">
      <GenericRegModul
          :key="`module-${mapperId}`"
          :loading="loading"
          :saving="saving"
          :position="position"
          :maxPos="maxPos"
          :currentMod="currentModule"
          @prevStep="prevStep"
          @nextStep="onNextStep"
          @ignore="onIngoredClicked"
          @saving="onSaving">
        <template v-slot:header>
          <p>
            Bitte trage hier dein Erlebnisangebot ein. <br/>
            <br/>
            Falls du Inspirationen oder Ideen brauchst kannst du gerne
            <a
                style="color: blue"
                target="_blank"
                href="https://docs.google.com/document/d/1DoACKvb5GdbcfumOU1vLRAM_JXjA_bcdKblyuxDGCwA/edit?usp=sharing">
              hier
            </a>
            schauen.
          </p>
        </template>

        <template v-slot:main>
          <ListWithDialogMain
              :ref="`dialog-main-${moduleId}`"
              :dialogMeta="dialogMeta"
              :valdiationObj="$v"
              @validate="validate"/>
        </template>
      </GenericRegModul>
    </v-container>
    <v-container v-else>
      <Circual/>
    </v-container>
  </v-container>
</template>

<script>
import {
  maxLength, minLength, required, integer,
} from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';
import Circual from '@/components/loading/Circual.vue';

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
    Circual,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    loading: true,
    saving: false,
    moduleData: [],
    showError: false,
    data: {},
  }),
  validations: {
    data: {
      title: {
        required,
      },
      duration: {
        integer,
        required,
      },
      type: {
        required,
      },
      price: {
        required,
      },
      pricePerPerson: {
        required,
      },
      minPerson: {
        required,
      },
      maxPerson: {
        required,
      },
      freeText: {
        required,
        maxLength: maxLength(10000),
        minLength: minLength(10),
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    loadingRead: {
      get() {
        return !!this.loading;
      },
    },
    mapperId() {
      return this.currentModule.id;
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
            cols: 12,
          },
          {
            name: 'Erlebnisangebot Dauer (In Minuten)',
            techName: 'duration',
            tooltip: 'Wie lange geht dein Erlebnisangebot vorraussichtlich?',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'number',
            default: '',
          },
          {
            name: 'Art des Angebots*',
            techName: 'type',
            tooltip: 'Um welchen Typ handelt es sich bei diesem Erlebnisangebot.',
            icon: 'mdi-card-account-details-outline',
            lookupPath: '/event/choices/workshop-type/',
            lookupListDisplay: ['name'],
            mandatory: true,
            fieldType: 'enumCombo',
          },
          {
            name: 'Fixe Kosten',
            techName: 'price',
            tooltip: 'Trage die Kosten, die unabhänging der Teilnehmerzahl entstehen hier ein.',
            icon: 'mdi-cash',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
          {
            name: 'Teilnehmer Kosten',
            techName: 'pricePerPerson',
            tooltip: 'Trage hier die Kosten, die pro Teilnehmer entstehen hier ein.',
            icon: 'mdi-cash',
            mandatory: true,
            fieldType: 'currency',
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
            fieldType: 'number',
            default: '',
          },
          {
            name: 'Wiederholbar?',
            techName: 'canBeRepeated',
            tooltip: 'Kann dein Erlebnisangebot mehrmals durch geführt werden?',
            icon: 'mdi-eye',
            fieldType: 'checkbox',
            default: '',
          },
          {
            name: 'Erlebnisangebot-Beschreibung',
            techName: 'freeText',
            tooltip: 'Beschreibe dein Erlebnisangebot möglichst genau. '
                + '(Wenn du Materialien benötigst, list sie hier auf.)',
            icon: 'mdi-text',
            mandatory: true,
            fieldType: 'textarea',
            default: '',
            counter: 10000,
            cols: 12,
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
      Promise.all([this.getModule(this.mapperId, this.currentEvent.id)])
        .then((values) => {
            this.moduleData = values[0].data; //eslint-disable-line
        })
        .catch((error) => {
          let errorMsg = error.response.data;
          if (error.response.data.detail) {
            errorMsg = error.response.data.detail;
          }
          this.$root.globalSnackbar.show({
            message: errorMsg,
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
          this.$nextTick(() => {
            const ref = `dialog-main-${this.moduleId}`;
            this.$refs[ref].beforeTabShow();
          });
        });
    },
  },
};
</script>
