<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
  >
    <template v-slot:header>
      Bitte trage hier ein wieviele Lager T-Shirts du haben willst.
    </template>

    <template v-slot:main>
      <v-row>
        <v-col cols="3" v-for="(item, index) in moduleData" :key="index">
          <v-text-field
            type="number"
            v-model="data[item.attribute.id]"
            :label="item.title"
          >
          </v-text-field>
        </v-col>
      </v-row>
    </template>
  </GenericRegModul>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
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
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    isLoading: true,
    moduleData: [],
    attributes: [],
    data: {},
    modulePath: '/event/event/',
  }),
  validations: {
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
              },
            ),
          );
        } else {
          if (this.data[moduleItem.attribute.id] !== null) { // eslint-disable-line
            promises.push(
              axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
                templateId: moduleItem.attribute.id,
                integerField: this.data[moduleItem.attribute.id],
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
        return value[0].integerField;
      }
      return item.defaultValue;
    },
    setDefaults() {
      this.moduleData.forEach((item) => {
        this.data[item.attribute.id] = this.getAttributeValue(item);
      });
    },
    loadData() {
      this.isLoading = true;
      Promise.all([
        this.getModule(this.currentModule.id, this.currentEvent.id),
        axios.get(`${process.env.VUE_APP_API}/${this.path}`),
      ])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.attributes = values[1].data; //eslint-disable-line
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
