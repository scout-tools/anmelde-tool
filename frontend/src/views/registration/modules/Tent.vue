<template>
  <GenericRegModul
    :key="`module-${currentModule.id}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
  >
    <template v-slot:header>
      <p>
        Bitte gebe an mit wievielen Zelten ihr kommen wollt.
        <br />
      </p>
    </template>

    <template v-slot:main>
      <v-row>
        <v-col cols="6" v-for="(item, index) in moduleData" :key="index">
          <p>{{ item.text }}</p>
          <v-text-field
            type="number"
            v-model="data[item.attribute.id]"
            :label="item.title"
            @input="checkNeedStangen()"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <p
          class="text-center"
          v-if="needStangen"
          style="border-style: solid; border-color: red"
        >
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-spin
          </v-icon>
          Zeltstangen sind nur begrenzt verfügbar. Bitte nutzt Steckstangen,
          wenn ihr welche zur Verfügung habt.
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
          Mega Cool, dass ihr eure Zeltstangen selbst mitbringt.
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline mdi-flip-h
          </v-icon>
        </p>
      </v-row>
    </template>
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
    isLoading: true,
    moduleData: [],
    attributes: [],
    needStangen: false,
    data: {},
  }),
  validations: {
    data: {},
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
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
    },
  },
  methods: {
    checkNeedStangen() {
      this.needStangen = //eslint-disable-line
        this.data && (this.data['18'] > 0 || this.data['20'] > 0);
    },
    beforeTabShow() {
      this.loadData();
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
      this.checkNeedStangen();
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
          promises.push(
            axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
              templateId: moduleItem.attribute.id,
              integerField: this.data[moduleItem.attribute.id],
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
  },
};
</script>
