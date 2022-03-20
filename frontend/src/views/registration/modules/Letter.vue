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
      <p>Hier ist Platz für eine Nachricht an die Lagerleitung</p>
    </template>

    <template v-slot:main>
      <div v-for="(field, i) in fields" :key="i">
        <BaseField
          :field="field"
          v-model="data[field.techName]"
          :valdiationObj="$v"
        />
      </div>
    </template>
  </GenericRegModul>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
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
    BaseField,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    isLoading: true,
    moduleData: [],
    xxx: {},
    data: {},
    modulePath: '/event/event/',
  }),
  validations: {
    data: {},
  },
  computed: {
    ...mapGetters(['userinfo']),
    fields() {
      if (!this.moduleData || !this.moduleData.length) {
        return [];
      }
      console.log(this.moduleData[0]);
      return [
        {
          name: this.moduleData[0].text,
          techName: 'freeText',
          tooltip: '123',
          icon: 'mdi-forum',
          mandatory: true,
          fieldType: 'textarea',
          cols: 12,
          default: '',
        },
      ];
    },
    isLoadingRead: {
      // getter
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
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    nextStep() {
      if (this.data.freeText && this.data.freeText.length > 0) {
        axios
          .post(`${process.env.VUE_APP_API}/${this.path}`, {
            templateId: this.moduleData[0].attribute.id,
            stringField: this.data.freeText,
            resourcetype: this.moduleData[0].attribute.resourcetype,
          })
          .then((response) => {
            console.log(response);
            this.$emit('nextStep');
          });
      } else {
        this.$emit('nextStep');
      }
    },
    setDefaults() {},
    loadData() {
      this.isLoading = true;
      Promise.all([
        this.getModule(this.currentModule.id),
        axios.get(`${process.env.VUE_APP_API}/${this.path}`),
      ])
        .then((values) => {
          debugger;
          this.moduleData = values[0].data; //eslint-disable-line
          this.attributes = values[1].data; //eslint-disable-line
          this.isLoading = false;
          this.setDefaults();
          this.loadAttributeEventModule();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    loadAttributeEventModule() {},
  },
};
</script>
