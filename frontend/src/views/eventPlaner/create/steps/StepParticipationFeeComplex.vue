<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :saving="saving"
    :loading="loading"
    :position="position"
    :maxPos="maxPos"
    @submit="submit"
    @ignore="onIngoredClicked"
    @prevStep="prevStep"
    @nextStep="nextStep"
    @saving="onSaving"
  >
    <template v-slot:header>
      Hier kannst du Rollen und Preise für dein Lager anlegen.
    </template>

    <template v-slot:main>
      <ListWithDialogMain
        :ref="'dialog-main-fee-complex'"
        :dialogMeta="dialogMeta"
        :valdiationObj="$v"
        :currentEvent="currentEvent"
        @validate="validate"
      />
    </template>
  </GenericRegModul>
</template>

<script>
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';

export default {
  name: 'StepParticipationFeeComplex',
  header: 'Teilnehmer_innen Beitrag',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'event',
    'currentRegistration',
    'currentModule',
    'personalData',
  ],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    GenericRegModul,
    ListWithDialogMain,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    saving: false,
    loading: true,
    selectedItem: 1,
    moduleData: [],
    data: {},
    moduleId: 1,
  }),
  validations: {
    data: {},
  },
  computed: {
    dialogMeta() {
      return {
        title: 'Hallo',
        listDisplay: ['name', 'price'],
        path: `event/event/${this.event.id}/booking-options`,
        fields: [
          {
            name: 'Name*',
            techName: 'name',
            tooltip: 'Name deiner Buchungsoption.',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Beschreibung*',
            techName: 'description',
            tooltip: 'Beschreibung deiner Buchungsoption.',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Preis*',
            techName: 'price',
            tooltip: 'Was kostet die Buchungsoption.',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
          {
            name: 'Buchbar von*',
            techName: 'bookableFrom',
            tooltip: 'Ab welchem Datum die diese Option buchbar?',
            mandatory: true,
            fieldType: 'datetime',
            default: '',
            cols: 12,
          },
          {
            name: 'Buchbar bis',
            techName: 'bookableTill',
            tooltip: 'Bis zu welchem Datum die diese Option buchbar?',
            mandatory: true,
            fieldType: 'datetime',
            default: '',
            cols: 12,
          },
        ],
      };
    },
  },
  methods: {
    beforeTabShow() {
      const me = this;
      this.loadData();
      setTimeout(() => {
        me.$refs['dialog-main-fee-complex'].beforeTabShow();
      }, 500);
    },
    loadData() {
      this.saving = false;
      this.loading = false;
    },
  },
};
</script>
