<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
  >
    <v-card :loading="loading">
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Modul bearbeiten</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-card-title>
                Module Name: {{ module && module.header }}
              </v-card-title>
            </v-row>
            <v-row>
              <template v-for="(field, i) in fields">
                <BaseField
                  :key="i"
                  :field="field"
                  v-model="data[field.techName]"
                  :valdiationObj="$v"
                />
              </template>
            </v-row>
          </v-container>
          <v-card-title> Verknüpfte Attribute: </v-card-title>
          <AttributeList
            :items="attributeMappers"
            :moduleMapper="moduleMapper"
            :ref="`dialog-main`"
            @refresh="onRefresh()"
          />
          <v-divider class="my-3" />
          <v-btn color="primary" @click="onClickOkay"> Speichern</v-btn>
        </v-form>
      </v-container>
      <v-divider class="my-4" />

      <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
        {{ errorText }}
      </v-snackbar>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios';
import { maxLength } from 'vuelidate/lib/validators';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import AttributeList from '@/components/dialog/attributeList/Main.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  props: ['isOpen'],
  mixins: [apiCallsMixin],
  components: {
    AttributeList,
    BaseField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    moduleMapper: null,
    module: null,
    attributeMappers: [],
    showError: false,
    errorText: 'Fehler beim Erstellen des Modules',
    showSuccess: false,
    timeout: 7000,
    loading: false,
    data: {
      overwriteDescription: '',
    },
    fields: [
      {
        name: 'Modul-Beschreibung (Optional)',
        techName: 'overwriteDescription',
        tooltip: 'Dieser Text überschreibt die Standard-Beschreibung.',
        mandatory: true,
        fieldType: 'html',
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      overwriteDescription: {
        maxLength: maxLength(10000),
      },
    },
  },

  computed: {},
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
    openDialog() {
      this.active = true;
    },
    onRefresh() {
      this.openDialogEdit(this.moduleMapper);
    },
    openDialogEdit(moduleMapper) {
      this.loading = true;
      const urlMapper = `${this.API_URL}/event/event/${moduleMapper.event}/event-module-mapper/${moduleMapper.id}/`;
      const urlModule = `${this.API_URL}/event/event-module/${moduleMapper.module.id || moduleMapper.module}/`;
      const urlAttributesMapper = `${this.API_URL}/event/event/${moduleMapper.event}/event-module-mapper/${moduleMapper.id}/attribute-mapper/`;
      // const urlAttributes =
      // `${this.API_URL}/event/event-module-mapper/${moduleMapper.id}/attributes/`;
      axios
        .all([
          axios.get(urlMapper),
          axios.get(urlModule),
          axios.get(urlAttributesMapper),
          // axios.get(urlAttributes),
        ])
        .then(
          axios.spread((firstResponse, secondResponse, thirdResponse) => {
            this.moduleMapper = firstResponse.data;
            this.module = secondResponse.data;
            this.attributeMappers = thirdResponse.data;
            this.data.overwriteDescription = this.moduleMapper.overwriteDescription;
          }),
        )
        .catch((error) => {
          console.log(error);
          this.errorText = 'Fehler beim laden des Moduls';
          this.showError = true;
        })
        .finally(() => {
          this.active = true;
          this.isEditWindow = true;
          this.loading = false;
        });
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
    onDescriptionSave() {
      this.updateEventModule(
        {
          overwriteDescription: this.data.overwriteDescription,
        },
        this.moduleMapper.id,
        this.moduleMapper.event,
      ).then(() => {
        this.closeDialog();
      });
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.onDescriptionSave();
        } catch (e) {
          console.log(e);
          this.errorText = 'Fehler beim Erstellen des Modules';
          this.showError = true;
        }
      } else {
        this.errorText = 'Feld ist zu lang.';
        this.showError = true;
      }
    },
  },
  created() {},
};
</script>
