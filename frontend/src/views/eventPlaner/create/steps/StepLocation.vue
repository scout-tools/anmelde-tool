<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :loading="loading"
    :saving="saving"
    :position="position"
    :maxPos="maxPos"
    @submit="submit"
    @ignore="onIngoredClicked"
    @prevStep="prevStep"
    @nextStep="nextStep"
    @saving="onSaving"
  >
    <template v-slot:header>
      Hier kannst du den Veranstaltungort anlegen.
    </template>

    <template v-slot:main>
      <ListWithDialogMain
        :ref="`dialog-main-location`"
        :dialogMeta="dialogMeta"
        :valdiationObj="$v"
        :currentEvent="currentEvent"
        @validate="validate"
        v-model="selectedItem"
      />
    </template>
  </GenericRegModul>
</template>

<script>
import { required, minLength } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';

export default {
  name: 'StepLocation',
  header: 'Veranstaltungsort',
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
    loading: true,
    saving: false,
    selectedItem: null,
    moduleData: [],
    data: {},
    locations: [],
    moduleId: 1,
  }),
  validations: {
    data: {
      name: {
        required,
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    dialogMeta() {
      return {
        title: 'Hallo',
        listDisplay: ['name'],
        path: 'event/event-location',
        fields: [
          {
            name: 'Name*',
            techName: 'name',
            tooltip: 'Name des Veranstaltungortes.',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Beschreibung*',
            techName: 'description',
            tooltip: 'Beschreibung des Veranstaltungortes.',
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
            name: 'Adresse*',
            techName: 'address',
            tooltip: 'Adresse des Veranstaltungortes',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Name Ansprechpartner*',
            techName: 'contactName',
            tooltip: 'Name des Ansprechpartners für den Veranstaltungort',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'E-Mail Ansprechpartner*',
            techName: 'contactEmail',
            tooltip: 'E-Mail des Ansprechpartners für den Veranstaltungort',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Telefonnummer Ansprechpartner*',
            techName: 'contactPhone',
            tooltip:
              'Telefonnummer des Ansprechpartners für den Veranstaltungort',
            mandatory: true,
            fieldType: 'textfield',
            default: 'textfield',
          },
          {
            name: 'Kosten pro Person',
            techName: 'perPersonFee',
            tooltip: '',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
          {
            name: 'Fixkosten',
            techName: 'fixFee',
            tooltip: '',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    nextStep() {
      this.patchService('location', this.locations[this.selectedItem].id, '/event/event/', this.event.id).then(
        () => {
          this.$emit('nextStep');
        },
      );
    },
    submit() {
      this.patchService('location', this.locations[this.selectedItem].id, '/event/event/', this.event.id).then(
        () => {
          this.$emit('submit');
        },
      );
    },
    beforeTabShow() {
      this.loadData();
      setTimeout(() => {
        this.$refs['dialog-main-location'].beforeTabShow();
      }, 100);
    },
    validate(data) {
      this.data = data;
      this.$v.$touch();
    },
    setDefaults() {},
    loadData() {
      Promise.all([
        this.getServiceById('event/event', this.id),
        this.getEventLocation(),
      ]).then((responses) => {
        this.locations = responses[1].data;
        const location = this.locations.filter(
          (item) => item.id === responses[0].data.location,
        )[0];
        this.selectedItem = this.locations.indexOf(location);
        this.$forceUpdate();
        this.saving = false;
        this.loading = false;
      });
    },
  },
  created() {
    this.beforeTabShow();
  },
  watch: {
    selectedItem() {
    },
  },
};
</script>
