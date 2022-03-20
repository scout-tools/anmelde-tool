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
            tooltip:
              '',
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
            tooltip:
              '',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
      console.log(this.$refs[`dialog-main-${this.moduleId}`]);
      // this.$refs[`dialog-main-${this.moduleId}`].beforeTabShow();
    },
    setDefaults() {},
    loadData() {
    },
  },
  created() {
    this.beforeTabShow();
  },
};
</script>
