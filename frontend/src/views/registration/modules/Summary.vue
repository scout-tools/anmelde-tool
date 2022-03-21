<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @submit="submitStep"
  >
    <template v-slot:header>
          <p><b>Zusammenfassung</b></p>
            Ich habe folgende Daten eingefügt:
    </template>

    <template v-slot:main>
      <v-row v-for="checkbox in moduleData" :key="checkbox.id">
        <v-checkbox
          v-model="data.checkboxes[checkbox.id]"
          :label="checkbox.text ? checkbox.text : ''"
          :error-messages="errorMessage('checkboxes', $v)"
        >
        </v-checkbox>
      </v-row>
    </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';

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
    isLoading: true,
    moduleData: [],
    data: {
      checkboxes: [],
    },
  }),
  validations: {
    data: {
      checkboxes: {
        required,
        allChecked: (value) => {
          const values = Object.values(value);
          console.log(values && values.every((item) => item));
          return values && values.every((item) => item);
        },
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    isLoadingRead: {
      // getter
      get() {
        return !!this.isloading;
      },
      set() {},
    },
    moduleId() {
      return this.currentModule.id;
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
    setDefaults() {
      this.moduleData.forEach((data) => {
        this.data.checkboxes[data.id] = false;
      });
    },
    onNextStep() {
      this.nextStep();
    },
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
