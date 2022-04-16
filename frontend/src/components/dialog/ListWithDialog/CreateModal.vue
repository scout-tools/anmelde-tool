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
  }),
  computed: {},
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
    openDialogEdit(item) {
      this.active = true;
      this.isEditWindow = true;
      if (item.id) {
        this.data.id = item.id;
        this.getData(item.id);
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
      this.valid = !this.valdiationObj.$anyError;
    },
    onClickOkay() {
      this.$emit('validate', this.data);
      this.$forceUpdate();
      this.validate();
      if (this.valid) {
        try {
          this.callCreateService();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    getData(id) {
      this.getServiceById(this.dialogMeta.path, id).then((response) => {
        this.data = response.data;
        this.isLoading = false;
      });
    },
    async callCreateService() {
      if (!this.isEditWindow) {
        this.createServiceById(this.dialogMeta.path, this.data).then(() => {
          this.closeDialog();
          this.$emit('refresh');
          this.$root.globalSnackbar.show({
            message:
              'Neuer Eintrag angelegt',
            color: 'success',
          });
        }).catch((error) => {
          let errorMessage = 'Es ist ein Fehler beim speichern aufgetreten.';
          const errorData = error.response.data;
          try {
            errorMessage = '';
            const keys = Object.keys(errorData);
            keys.forEach((key) => {
              errorMessage += `Fehler bei ${key}: ${errorData[key]}  -  `;
            });
          } catch {
            console.log('Fehler');
          }
          this.$root.globalSnackbar.show({
            message: errorMessage,
            color: 'error',
          });
        });
      } else {
        this.updateServiceById(this.dialogMeta.path, this.data).then(() => {
          this.closeDialog();
          this.$emit('refresh');
        });
      }
    },
  },
  created() {
    this.isLoading = true;
  },
};
</script>
