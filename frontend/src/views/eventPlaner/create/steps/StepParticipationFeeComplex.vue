<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @submit="submit"
    @ignore="onIngoredClicked"
    @prevStep="prevStep"
    @nextStep="nextStep"
  >
    <template v-slot:header>
      Hier kannst du Rollen und Preise für dein Lager anlegen.
    </template>

    <template v-slot:main>
      <ListWithDialogMain
        :ref="'dialog-main-fee-complex'"
        :dialogMeta="dialogMeta"
        :valdiationObj="$v"
      />
    </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';
// import CreateSinglePersonDialog from '../dialog/CreateSinglePersonDialogBundesfahrt.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';

export default {
  name: 'StepParticipationFeeComplex',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos', 'event'],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    GenericRegModul,
    ListWithDialogMain,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    selectedItem: 1,
    moduleData: [],
    data: {},
    moduleId: 1,
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
    dialogMeta() {
      return {
        title: 'Hallo',
        listDisplay: ['name', 'price'],
        path: `event/event/${this.event.id}/booking-options`,
        fields: [
          {
            name: 'Name*',
            techName: 'name',
            tooltip: '',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Beschreibung*',
            techName: 'description',
            tooltip: '',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Preis*',
            techName: 'price',
            tooltip: '',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
          {
            name: 'Buchbar von*',
            techName: 'bookableFrom',
            tooltip: '',
            mandatory: true,
            fieldType: 'datetime',
            default: '',
            cols: 12,
          },
          {
            name: 'Buchbar bis',
            techName: 'bookableTill',
            tooltip: '',
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
      this.loadData();
      console.log(this.$refs['dialog-main-fee-complex']);
      setTimeout(() => {
        this.$refs['dialog-main-fee-complex'].beforeTabShow();
      }, 100);
    },
    setDefaults() {},
    loadData() {},
  },
  created() {
    this.beforeTabShow();
  },
};
</script>
