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
    <template v-slot:header> </template>

    <template v-slot:main> </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';

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
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    loading: true,
    saving: false,
    moduleData: [],
    attributes: [],
    data: {},
  }),
  validations: {
    data: {},
  },
  computed: {
    ...mapGetters(['userinfo']),
    loadingRead: {
      // getter
      get() {
        return !!this.loading;
      },
      set() {},
    },
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
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
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    setDefaults() {},
    loadData() {
      this.saving = false;
      this.loading = true;
      Promise.all([
        this.getModule(this.currentModule.id, this.currentEvent.id),
        axios.get(`${process.env.VUE_APP_API}/${this.path}`),
      ])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.attributes = values[1].data; //eslint-disable-line
          this.loading = false;
          this.setDefaults();
          this.loadAttributeEventModule();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
  },
};
</script>
