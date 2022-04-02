<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Eintrag</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row>
          <template v-for="(field, i) in dialogMeta.fields">
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
  </v-dialog>
</template>

<script>
import axios from 'axios';

import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';

export default {
  components: {
    BaseField,
  },
  props: {
    dialogMeta: {
      default: {},
    },
    valdiationObj: {
      default: {},
    },
    moduleMapper: {
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
  }),
  computed: {
    path() {
      return `${this.API_URL}/event/event/${this.dialogMeta.regId}/event-module-mapper/${this.moduleMapper.id}/attribute-mapper/`;
    },
    attributeMapperId() {
      return this.data.id;
    },
  },
  methods: {
    openDialog() {
      this.active = true;
      this.isEditWindow = false;
    },
    openDialogEdit(id) {
      this.active = true;
      this.isEditWindow = true;
      if (id) {
        this.data.id = id;
        this.getData(id);
      } else {
        this.setDefaults();
      }
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
      this.valid = true; // !this.valdiationObj.$anyError;
    },
    onClickOkay() {
      // this.validate();
      if (this.valid) {
        try {
          this.callCreateService();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    getData() {
      axios
        .get(`${this.path}/${this.attributeMapperId}/`) // eslint-disable-line
        .then((response) => {
          this.data = response.data;
        });
    },
    async callCreateService() {
      if (!this.isEditWindow) {
        axios
          .post(this.path, {
            title: this.data.title,
            text: this.data.text,
          })
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      } else {
        axios
          .put(`${this.path}/${this.attributeMapperId}/`, {
            title: this.data.title,
            text: this.data.text,
          })
          .then(() => {
            this.closeDialog();
            this.$emit('refresh');
          });
      }
    },
  },
  created() {},
};
</script>
