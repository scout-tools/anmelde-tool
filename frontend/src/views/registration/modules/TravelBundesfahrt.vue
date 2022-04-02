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
      <p>Wann und wie werdet ihr voraussichtlich an ankommen?</p>
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
      <p
        class="text-center"
        v-if="withCar"
        style="border-style: solid; border-color: red"
      >
        <v-icon color="red darken-1" large class="ma-2">
          mdi-alert mdi-spin
        </v-icon>
          Bitte bildet Fahrgemeinschalten
        <v-icon color="red darken-1" large class="ma-2">
          mdi-alert mdi-flip-h mdi-spin
        </v-icon>
      </p>
    </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import BaseField from '@/components/common/BaseField.vue';

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
    BaseField,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    loading: true,
    saving: false,
    moduleData: [],
    attributes: [],
    data: {
      vehicle: '',
      time: '',
    },
    fields: [
      {
        name: 'Verkehrsmittel*',
        techName: 'vehicle',
        tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
        icon: 'mdi-train-car',
        mandatory: true,
        lookupPath: '/basic/travel-type-choices/',
        lookupListDisplay: ['name'],
        fieldType: 'enumCombo',
        multiple: false,
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      vehicle: {
        required,
      },
    },
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
    moduleId() {
      return this.currentModule.module.id;
    },
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
    },
    withCar() {
      return this.data.vehicle && this.data.vehicle === 'C';
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    setDefaults() {
      this.moduleData.forEach((item) => {
        if (item && item.attribute.resourcetype === 'TravelAttribute') {
          this.data.vehicle = this.getAttributeValue(item)[0]; //eslint-disable-line
          this.data.time = this.getAttributeValue(item)[1]; //eslint-disable-line
        }
      });
    },
    getAttributeValue(item) {
      const value = this.attributes.filter(
        (att) => att.templateId === item.attribute.id,
      );
      if (value && value.length) {
        return [value[0].typeField, value[0].timeField];
      }
      return [null, null];
    },
    onNextStep(force) {
      this.saving = true;
      const promises = [];
      this.validate();
      if (!this.valid) {
        this.saving = false;
        return;
      }
      this.moduleData.forEach((moduleItem) => {
        const getAtt = this.attributes.filter(
          (att) => att.templateId === moduleItem.attribute.id,
        );
        if (getAtt.length > 0) {
          if (moduleItem && moduleItem.attribute.resourcetype === 'TravelAttribute') {
            promises.push(
              axios.put(
                `${process.env.VUE_APP_API}/${this.path}${getAtt[0].id}/`,
                {
                  timeField: this.data.time,
                  typeField: this.data.vehicle,
                },
              ),
            );
          }
        } else {
          if (moduleItem && moduleItem.attribute.resourcetype === 'TravelAttribute') { //eslint-disable-line
            promises.push(
              axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
                templateId: moduleItem.attribute.id,
                timeField: this.data.time,
                typeField: this.data.vehicle,
                resourcetype: moduleItem.attribute.resourcetype,
              }),
            );
          }
        }
      });
      if (promises.length > 0 || force) {
        Promise.all(promises).then(() => {
          this.$emit('nextStep');
        });
      } else {
        this.$emit('nextStep');
      }
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
          console.error(error.response);
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
  },
};
</script>
