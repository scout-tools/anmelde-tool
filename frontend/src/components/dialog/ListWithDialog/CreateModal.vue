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
              :valdiationObj="$v"
            />
          </template>
        </v-row>
        <v-divider class="my-3" />
        <v-btn color="primary" @click="onClickOkay"> Speichern</v-btn>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ 'Fehler beim Erstellen des Ortes' }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
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
  validations: {
    data: {
      firstName: {
        required,
      },
    },
  },
  computed: {},
  methods: {
    openDialog() {
      this.active = true;
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
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateService();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    getData(id) {
      const regId = this.$route.params.id;
      this.getRegServiceById('single-participant', regId, id).then(
        (response) => {
          this.data = response.data;
        },
      );
    },
    async callCreateService() {
      const modulePath = 'single-participant';
      const regId = this.$route.params.id;
      const path = `/event/registration/${regId}/single-participant/`;
      if (!this.isEditWindow) {
        axios.post(this.API_URL + path, this.data).then(() => {
          this.closeDialog();
          this.$emit('refresh');
        });
      } else {
        this.updateRegServiceById(modulePath, regId, this.data).then(() => {
          this.closeDialog();
          this.$emit('refresh');
        });
      }
    },
  },
  created() {},
};
</script>