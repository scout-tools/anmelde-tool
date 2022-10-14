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
          <v-col cols="4">
          <v-autocomplete
            clearable
            :loading="loading"
            :items="personList"
            v-model="person"
            label="Filter nach Buchoptionen"
            :item-text="getPersonText"
            item-value="id"
            no-data-text="Keine Buchoptionen gefunden."
          />
          </v-col>
        </v-row>
        <v-divider class="my-3" />
        <v-btn color="success" @click="onClickOkay"> Anmelden</v-btn>
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
import axios from 'axios';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import Circual from '@/components/loading/Circual.vue';

export default {
  components: {
    Circual,
  },
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {},
    person: null,
    loading: true,
    personList: [],
    personalData: null,
    isLoading: false,
    timeout: 3000,
    showError: false,
  }),
  methods: {
    getPersonText(item) {
      return `${item.firstName} ${item.lastName}`;
    },
    getData() {
      this.loading = true;
      Promise.all([this.getPersons()])
        .then((values) => {
          this.personList = values[0].data;
          this.getPeronalData();
        })
        .catch((err) => {
          this.$root.globalSnackbar.show({
            message: err.data,
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
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
    onClickOkay() {
      this.$emit('openPerson', this.personList.filter((item) => item.id === this.person)[0]);
    },
    getPeronalData() {
      const path = `${this.API_URL}/auth/personal-data/`;
      axios
        .get(path)
        .then((res) => {
          this.personalData = res.data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Es gab einen Fehler beim runterladen deiner Daten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
