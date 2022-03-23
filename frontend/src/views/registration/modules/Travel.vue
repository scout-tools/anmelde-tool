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
          v-if="data.vehicle && data.vehicle.value === 'C'"
          style="border-style: solid; border-color: red"
        >
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-spin
          </v-icon>
          Bitte beachtet, dass vor Ort selbst nur sehr wenige bis keine
          Parkplätze zur Verfügung stehen und PKW daher ggf. in einiger
          Entfernung im Umland abgestellt werden müssen.
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-flip-h mdi-spin
          </v-icon>
        </p>
        <p
          class="text-center"
          v-else
          style="border-style: solid; border-color: green"
        >
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline
          </v-icon>
          Mega Cool, dass ihr ohne Auto anreist.
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline mdi-flip-h
          </v-icon>
        </p>
      <!-- <v-row cols="12" class="py-2">
        <p>Wann werdet ihr voraussichtlich an ankommen?</p>

        <v-btn-toggle v-model="data.time" tile color="blue accent-3" group>
          <v-btn value="left"> 16:00 - 18:00</v-btn>

          <v-btn value="center"> 18:00 - 20:00</v-btn>
          <v-btn value="right"> 20:00 - 22:00 </v-btn>
          <v-btn value="123"> 22:00 - 0:00 </v-btn>
          <v-btn value="later"> Noch Später</v-btn>
        </v-btn-toggle>
      </v-row>
      <p>Wie werdet ihr anreisen?</p>
      <v-row>
        <v-col cols="4" sm="8">
          <v-btn-toggle
            v-model="data.vehicle"
            tile
            color="blue accent-3"
            group
            multiple
          >
            <v-btn value="tain"> Bahn </v-btn>

            <v-btn value="bus"> Reisebus </v-btn>
            <v-btn value="car"> PKW </v-btn>
            <v-btn value="else"> Sonstiges </v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('car')"
            label="Wieviele PKWs?"
          >
          </v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('else')"
            label="Sonstiges Vekehrsmittel"
          >
          </v-text-field>
        </v-col>
      </v-row> -->
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
    isLoading: true,
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
      {
        name: 'Zeipunkt*',
        techName: 'time',
        tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
        icon: 'mdi-clock',
        mandatory: true,
        lookupPath: '/basic/travel-slots-choices/',
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
      time: { required },
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
    setDefaults() {
      this.moduleData.forEach((item) => {
        this.data.vehicle = this.getAttributeValue(item)[0].value; //eslint-disable-line
        this.data.time = this.getAttributeValue(item)[1].value; //eslint-disable-line
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
                timeField: this.data.time.value,
                typeField: this.data.vehicle.value,
              },
            ),
          );
        } else {
          promises.push(
            axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
              templateId: moduleItem.attribute.id,
              timeField: this.data.time.value,
              typeField: this.data.vehicle.value,
              resourcetype: moduleItem.attribute.resourcetype,
            }),
          );
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
          console.error(error.response);
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
