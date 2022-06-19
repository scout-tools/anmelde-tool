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
      <p>Bitte trage den Modultext ein.</p>
    </template>

    <template v-slot:main>
      <v-row>
        <v-col cols="12" v-for="(item, index) in moduleData" :key="index">
          <BaseField
            :key="index"
            :field="{
              name: item.title,
              techName: item.attribute.id,
              tooltip: item.tooltip,
              icon: item.icon,
              mandatory: true,
              fieldType: item.fieldType,
              default: item.defaultValue,
            }"
            v-model="data[item.attribute.id]"
            :valdiationObj="$v"
          />
        </v-col>
      </v-row>
    </template>
  </GenericRegModul>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import BaseField from '@/components/common/BaseField.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';

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
    loading: true,
    saving: false,
    moduleData: [],
    attributes: [],
    data: {},
    modulePath: '/event/event/',
  }),
  validations: {},
  computed: {
    ...mapGetters(['userinfo']),
    loadingRead: {
      // getter
      get() {
        return !!this.loading;
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
    onNextStep() {
      this.saving = true;
      const promises = [];
      this.moduleData.forEach((moduleItem) => {
        const getAtt = this.attributes.filter(
          (att) => att.templateId === moduleItem.attribute.id,
        );
        if (getAtt.length > 0) {
          promises.push(
            axios.put(
              `${process.env.VUE_APP_API}/${this.path}${getAtt[0].id}/`,
              {
                integerField: this.data[moduleItem.attribute.id],
                stringField: this.data[moduleItem.attribute.id],
                booleanField: this.data[moduleItem.attribute.id],
              },
            ),
          );
        } else {
          if (this.data[moduleItem.attribute.id] !== null) { // eslint-disable-line
            promises.push(
              axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
                templateId: moduleItem.attribute.id,
                integerField: this.data[moduleItem.attribute.id],
                stringField: this.data[moduleItem.attribute.id],
                booleanField: this.data[moduleItem.attribute.id],
                resourcetype: moduleItem.attribute.resourcetype,
              }),
            );
          }
        }
      });
      if (promises.length > 0) {
        Promise.all(promises).then(() => {
          this.nextStep();
        });
      } else {
        this.nextStep();
      }
    },
    getAttributeValue(item) {
      const value = this.attributes.filter(
        (att) => att.templateId === item.attribute.id,
      );
      if (value && value.length) {
        return value[0].integerField || value[0].stringField || value[0].booleanField;
      }
      return item.defaultValue;
    },
    setDefaults() {
      this.moduleData.forEach((item) => {
        this.data[item.attribute.id] = this.getAttributeValue(item);
      });
    },
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
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
  },
};
</script>
