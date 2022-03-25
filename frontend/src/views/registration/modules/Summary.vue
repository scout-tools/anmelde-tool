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
      <v-container>
        <v-row>
          <p>Ich habe folgende Daten eingefügt:</p>
        </v-row>
        <v-row>
          <v-list subheader>
            <v-subheader>Werte</v-subheader>
            <v-list-item v-for="(attribute, index) in attributes" :key="index">
              <v-list-item-content>
                <v-list-item-title>{{ attribute.name }}</v-list-item-title>
                <v-list-item-subtitle>{{
                  getValueField(attribute)
                }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-row>
        <v-row>
          <p>Gesamtpersonenanzahl: {{ summary.participantCount }}</p>
        </v-row>
        <v-row>
          <p>Gesamtpreis: {{ summary.price || 0 }} €</p>
        </v-row>
      </v-container>
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
    summary: [],
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
    attributes() {
      if (this.summary.tags) {
        return this.summary.tags.filter((item) => this.getValueField(item));
      }
      return [];
    },
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
    getValueField(item) {
      let value = '';
      if (item.booleanField) {
        value = item.booleanField;
      }
      if (item.integerField) {
        value = item.integerField;
      }
      if (item.stringField) {
        value = item.stringField;
      }
      console.log(value);
      switch (value) {
        case true:
          return 'Ja';
        case false:
          return 'Nein';
        default:
          return value;
      }
    },
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
      Promise.all([
        this.getModule(this.moduleId, this.currentEvent.id),
        this.getRegService('summary', this.currentRegistration.id),
      ])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.summary = values[1].data[0]; //eslint-disable-line
          this.isLoading = false;
          this.setDefaults();
          console.log(this.summary);
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
