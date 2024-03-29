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
      Wieviele Lunch Packete braucht ihr am Abreisetag??
    </template>

    <template v-slot:main>
      <template v-for="(field, index) in fields">
        <BaseField
          :key="index"
          :field="field"
          v-model="data[field.techName]"
          :valdiationObj="$v"
        />
      </template>
    </template>
  </GenericRegModul>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import {
  required,
} from 'vuelidate/lib/validators';
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
    loading: true,
    saving: false,
    moduleData: [],
    attributes: [],
    xxx: {},
    data: {},
    modulePath: '/event/event/',
  }),
  validations: {
    data: {
      lunchPackets: {
        required,
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    fields() {
      if (!this.moduleData || !this.moduleData.length) {
        return [];
      }
      return [
        {
          name: 'Lunch Packe',
          techName: 'lunchPackets',
          tooltip: 'Wieviele Lunchpackete braucht ihr bei der Abfahrt?',
          icon: 'mdi-food',
          mandatory: true,
          fieldType: 'number',
          default: 0,
        },
      ];
    },
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
                integerField: this.data.lunchPackets,
              },
            ),
          );
        } else {
          promises.push(
            axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
              templateId: moduleItem.attribute.id,
              integerField: this.data.lunchPackets,
              resourcetype: moduleItem.attribute.resourcetype,
            }),
          );
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
        this.data.lunchPackets = this.getAttributeValue(item);
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
