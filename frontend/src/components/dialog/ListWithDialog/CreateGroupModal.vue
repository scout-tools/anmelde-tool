<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card v-if="!isLoading">
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Eintrag</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row>
          <template v-for="(field, i) in fields">
            <BaseField
              :key="i"
              :field="field"
              v-model="data[field.techName]"
              :valdiationObj="valdiationObj"
            />
          </template>
        </v-row>
        <v-divider class="my-3" />
        <v-btn color="success" @click="onClickOkay"> Speichern</v-btn>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Erstellen des Ortes' }}
      </v-snackbar>
    </v-card>
    <v-container v-show="isLoading">
      <Circual />
    </v-container>
  </v-dialog>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';
import Circual from '@/components/loading/Circual.vue';

export default {
  components: {
    BaseField,
    Circual,
  },
  props: {
    dialogMeta: {
      default: {},
    },
    valdiationObj: {},
    currentRegistration: {
      default: {},
    },
  },
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {},
    showError: false,
    showSuccess: false,
    timeout: 7000,
    isLoading: true,
    mapping1: ['wolf', 'sippling', 'rover'],
    mapping2: ['Amount', 'Veggi', 'Vegan'],
    fields: [
      {
        name: 'Allesesser Wölflinge',
        techName: 'wolfAmount',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-human-child',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegetariche Wölflinge ',
        techName: 'wolfVeggi',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-cow-off',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegane Wölflinge',
        techName: 'wolfVegan',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-sprout',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Allesesser Sipplinge',
        techName: 'sipplingAmount',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-human-greeting',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegetariche Sipplinge',
        techName: 'sipplingVeggi',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-cow-off',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegane Sipplinge',
        techName: 'sipplingVegan',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-sprout',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Allesesser Rover_Innen',
        techName: 'roverAmount',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-account-cowboy-hat',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegetariche Rover_Innen',
        techName: 'roverVeggi',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-cow-off',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
      {
        name: 'Vegane Rover_Innen',
        techName: 'roverVegan',
        tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
        icon: 'mdi-sprout',
        mandatory: true,
        fieldType: 'number',
        default: '',
        cols: 4,
      },
    ],
  }),
  computed: {
    path() {
      return `event/registration/${this.currentRegistration.id}/add-group-participants`;
    },
  },
  methods: {
    openDialog(item) {
      this.active = true;
      this.isEditWindow = false;
      if (item) {
        this.data = item;
      } else {
        this.setDefaults();
      }
      this.$forceUpdate();
      this.isLoading = false;
    },
    setDefaults() {
      this.data = {};
    },
    closeDialog() {
      this.active = false;
      this.valdiationObj.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.valdiationObj.$touch();
      this.valid = !this.valdiationObj.$anyError;
    },
    onClickOkay() {
      this.callCreateService();
    },
    getData(id) {
      this.getServiceById(this.dialogMeta.path, id).then((response) => {
        this.data = response.data;
        this.isLoading = false;
      });
    },
    async callCreateService() {
      const promises = this.collectRequests();
      Promise.all(promises).then(() => {
        this.closeDialog();
        this.$emit('refresh');
        this.$root.globalSnackbar.show({
          message: 'Neuer Eintrag angelegt',
          color: 'success',
        });
      });
    },
    collectRequests() {
      const promises = [];
      const mapping = [
        {
          type: 'wolfAmount',
          scoutLevel: 'W',
          eatHabit: null,
        },
        {
          type: 'wolfVeggi',
          scoutLevel: 'W',
          eatHabit: 1,
        },
        {
          type: 'wolfVegan',
          scoutLevel: 'W',
          eatHabit: 2,
        },
        {
          type: 'sipplingAmount',
          scoutLevel: 'S',
          eatHabit: null,
        },
        {
          type: 'sipplingVeggi',
          scoutLevel: 'S',
          eatHabit: 1,
        },
        {
          type: 'sipplingVegan',
          scoutLevel: 'S',
          eatHabit: 2,
        },
        {
          type: 'roverAmount',
          scoutLevel: 'R',
          eatHabit: null,
        },
        {
          type: 'roverVeggi',
          scoutLevel: 'R',
          eatHabit: 1,
        },
        {
          type: 'roverVegan',
          scoutLevel: 'R',
          eatHabit: 2,
        },
      ];
      mapping.forEach((map) => {
        if (this.data[map.type] > 0) {
          promises.push(
            this.createServiceById(this.path, {
              number: this.data[map.type],
              scoutLevel: map.scoutLevel,
              eatHabit: map.eatHabit,
            }),
          );
        }
      });
      return promises;
    },
  },
  created() {
    this.isLoading = true;
  },
};
</script>
