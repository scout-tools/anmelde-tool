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
    @submit="submitStep"
    @saving="onSaving"
  >
    <template v-slot:header>
      Sobald du die Anmeldung abgeschickt hast,
      bekommst du eine E-Mail mit der Bestätigung. <br>
      <br>
    </template>

    <template v-slot:main>
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
                  }}
                </v-list-item-subtitle>
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
        <!--        <v-row v-for="checkbox in moduleData" :key="checkbox.id">-->
        <!--          <v-checkbox-->
        <!--            v-model="data.checkboxes[checkbox.id]"-->
        <!--            :label="checkbox.text ? checkbox.text : ''"-->
        <!--            :error-messages="errorMessage('checkboxes', $v)">-->
        <!--          </v-checkbox>-->
        <!--        </v-row>-->
        <v-row>
          <v-checkbox
            v-if="moduleData && moduleData.length && moduleData[0]"
            v-model="data.checkboxes[moduleData[0].id]"
            :label="getConfirmedText"
            :error-messages="errorMessage('checkboxes', $v)">
          </v-checkbox>
        </v-row>
      </v-container>
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
    loading: true,
    saving: false,
    moduleData: [],
    summary: [],
    confirmed: false,
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

          if (value && !value.length) {
            return true;
          }
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
    loadingRead: {
      // getter
      get() {
        return !!this.loading;
      },
      set() {
      },
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
    getConfirmedText() {
      if (this.currentRegistration.single) {
        return 'Ich habe meine Daten überprüft und melde mich verbindlich zur Fahrt an.';
      }
      return 'Ich habe meine Daten überprüft und melde meinen Stamm verbindlich zur Fahrt an.';
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
      this.saving = true;
      this.nextStep();
    },
    loadData() {
      this.saving = false;
      this.loading = true;
      Promise.all([
        this.getModule(this.moduleId, this.currentEvent.id),
        this.getRegService('summary', this.currentRegistration.id),
      ])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.summary = values[1].data[0]; //eslint-disable-line
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
