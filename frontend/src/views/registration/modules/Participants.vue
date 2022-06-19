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
      <p>
        Ich melde folgende Teilnehmende an <br />
        <br />
        Die Erfassung erfolgt pro Person oder als ganze Gruppe.
        Löschen und bearbeiten geht nur pro Person. <br />
        <br />
        <v-icon color="red"> mdi-alert-circle</v-icon>
        Du musst dich selbst auch in die Liste eintragen.
      </p>
    </template>

    <template v-slot:main>
    <v-tabs
      v-model="tab"
      background-color="transparent"
      grow
    >
      <v-tab>
        Stufen
      </v-tab>
      <v-tab>
        Essen
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Anmeldezahl</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in summary" :key="item.name">
              <td>{{ item.name }}</td>
              <td>{{ item.value }}</td>
            </tr>
          </tbody>
          <tfoot>
              <tr>
                  <th scope="row"><b>Gesamtanmeldezahl</b></th>
                  <td>{{ getSummaryDataByKey('participantCount') }}</td>
              </tr>
          </tfoot>
        </template>
      </v-simple-table>
      </v-tab-item>
      <v-tab-item>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">Name</th>
              <th class="text-left">Essenbesonderheiten</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in summaryEat" :key="item.name">
              <td>{{ item.name }}</td>
              <td>{{ item.value }}</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
      </v-tab-item>
    </v-tabs-items>
      <ListWithDialogMain
        :ref="`dialog-main-${moduleId}`"
        :currentRegistration="currentRegistration"
        :dialogMeta="dialogMeta"
        :valdiationObj="$v"
        @validate="validate"
        @refresh="refresh"
      />
    </template>
  </GenericRegModul>
</template>

<script>
import { required, minLength, maxLength } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';
import ListWithDialogMain from '@/components/dialog/ListWithDialog/Main.vue';

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
    ListWithDialogMain,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    loading: true,
    saving: false,
    moduleData: [],
    showError: false,
    data: {},
    summaryData: {},
    tab: null,
  }),
  validations: {
    data: {
      scoutName: {
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      scoutLevel: {
        required,
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    loadingRead: {
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
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: false,
        groupAdd: true,
        path: `event/registration/${this.currentRegistration.id}/single-participant`,
        listDisplay: ['scoutName', 'scoutLevel', 'eatHabit'],
        fields: [
          {
            name: 'Fahrtenname',
            techName: 'scoutName',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein. Das dient nur der Übersicht.',
            icon: 'mdi-campfire',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Stufe*',
            techName: 'scoutLevel',
            tooltip:
              'Wähle die Stufe der Person aus, die du anmeldest.',
            icon: 'mdi-account-circle',
            lookupPath: '/event/choices/scout-level-types/',
            lookupListDisplay: ['name'],
            mandatory: true,
            fieldType: 'enumCombo',
            default: '',
          },
          {
            name: 'Essenbesonderheiten',
            techName: 'eatHabit',
            tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
            icon: 'mdi-food',
            mandatory: true,
            lookupPath: '/basic/eat-habits/',
            lookupListDisplay: ['name'],
            fieldType: 'refCombo',
            default: '',
          },
        ],
      };
    },
    summary() {
      return [
        {
          name: 'Wölflinge',
          value: this.getSummaryDataByKey('wolfCount'),
        },
        {
          name: 'Sipplinge',
          value: this.getSummaryDataByKey('sipplingCount'),
        },
        {
          name: 'Rover_Innen',
          value: this.getSummaryDataByKey('roverCount'),
        },
      ];
    },
    summaryEat() {
      return [
        {
          name: 'Vegetarisch',
          value: this.getSummaryDataByKey('veggiCount'),
        },
        {
          name: 'Vegan',
          value: this.getSummaryDataByKey('veganCount'),
        },
      ];
    },
  },
  methods: {
    getSummaryDataByKey(key) {
      return this.summaryData[key] ? this.summaryData[key] : 0;
    },
    validate(data) {
      this.data = data;
      this.$v.$touch();
    },
    beforeTabShow() {
      this.refresh();
    },
    onNextStep() {
      this.saving = true;
      this.nextStep();
    },
    setDefaults() {},
    refresh() {
      this.loadData();
      if (this.$refs[`dialog-main-${this.moduleId}`]) {
        this.$refs[`dialog-main-${this.moduleId}`].beforeTabShow();
      }
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
          this.summaryData = values[1].data[0]; //eslint-disable-line
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
