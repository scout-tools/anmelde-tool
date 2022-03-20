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
          <v-container v-if="module && module.custom">
            <v-row>
              <v-text-field
                v-model="module.header"
                :counter="20"
                label="Name der Schlafstätte"
                required
                prepend-icon="mdi-earth"
                v-if="module && module.custom"
              >
                <template slot="append">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon color="success" dark v-bind="attrs" v-on="on">
                        mdi-help-circle-outline
                      </v-icon>
                    </template>
                    <span> Gib hier den Namen der Schlafstätte ein. </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-row>
            <v-row> </v-row>
          </v-container>
          <v-container v-else>
            <v-row>
              <v-card-title>
                Module Name: {{ module && module.header }}
              </v-card-title>
            </v-row>
            <v-row>
              <v-card-text v-if="moduleMapper && moduleMapper.overwriteDescription">
                {{ moduleMapper.overwriteDescription }}
              </v-card-text>
              <v-card-text v-else>
                Ein gibt keinen Individuellen Text.
              </v-card-text>
            </v-row>
          </v-container>
          <v-card-title> Verknüpfte Attribute: </v-card-title>
          <AttributeList
            :items="attributeMappers"
            :ref="`dialog-main`"
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
import {
  required,
  // minLength,
  numeric,
  // requiredIf,
} from 'vuelidate/lib/validators';
import axios from 'axios';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import AttributeList from '@/components/dialog/attributeList/Main.vue';

export default {
  props: ['isOpen'],
  mixins: [apiCallsMixin],
  components: {
    AttributeList,
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
  }),
  validations: {
    locationType: {
      required,
      numeric,
    },
  },

  computed: {},
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
    openDialog() {
      this.active = true;
    },
    openDialogEdit(moduleMapper) {
      this.loading = true;
      const urlMapper = `${this.API_URL}/event/event-module-mapper/${moduleMapper.id}/`;
      const urlModule = `${this.API_URL}/event/event-module/${moduleMapper.module.id}/`;
      const urlAttributesMapper = `${this.API_URL}/event/event-module-mapper/${moduleMapper.id}/attribute-mapper/`;
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
            console.log(firstResponse.data);
            console.log(secondResponse.data);
            console.log(thirdResponse.data);
            this.moduleMapper = firstResponse.data;
            this.module = secondResponse.data;
            this.attributeMappers = thirdResponse.data;
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
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateEventLocationPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
  },
  created() {},
};
</script>
