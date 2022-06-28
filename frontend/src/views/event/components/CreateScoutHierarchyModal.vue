<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Gruppe Erstellen</v-card-title>
          <v-card-text>
            <div class="ma-2">
              <p class="ma-0">
                Um Meute, Sippe oder Roverrunde zu erstellen,
                einfach den Namen mit dem Präfix Meute, Sippe oder Roverrunde eintragen.
              </p>
            </div>
            <v-container>
              <v-row>
                <template v-for="(field, i) in fields">
                  <BaseField
                      :key="i"
                      :field="field"
                      v-model="data[field.techName]"
                      :valdiationObj="$v"
                      @keydownEnter="onCreateScoutHierarchyClicked"/>
                </template>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn color="grey darken-1" text @click="cancel()">Zurück</v-btn>
            <v-btn color="success" text @click="onCreateScoutHierarchyClicked">
              Erstellen
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <v-snackbar v-model="showError" color="error" y="top">
      {{ errorMessage }}
    </v-snackbar>
  </div>
</template>

<script>
import axios from 'axios';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';
import { required } from 'vuelidate/lib/validators';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    showError: false,
    errorMessage: false,
    data: {
      name: '',
    },
  }),
  components: {
    BaseField,
  },
  mixins: [
    apiCallsMixin,
  ],
  methods: {
    show() {
      this.dialog = true;
    },
    cancel() {
      console.log('test');
      this.showError = false;
      this.errorMessage = '';
      this.dialog = false;
    },
    onCreateScoutHierarchyClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createScoutHierarchy();
    },
    createScoutHierarchy() {
      axios
        .post(`${this.API_URL}/event/registration-scouthierarchy/`, {
          name: this.data.name,
        })
        .then((response) => {
          console.log(response);
          this.$emit('created');
          this.cancel();
        })
        .catch((error) => {
          console.log(error);
          this.showError = true;
          this.errorMessage = error.response.data;
        });
    },
  },
  validations: {
    data: {
      name: {
        required,
      },
    },
  },
  computed: {
    fields() {
      return [
        {
          name: 'Name deiner Gruppe',
          techName: 'name',
          lookupPath: `/event/registration-scouthierarchy/?level=${this.registrationLevelId}`,
          tooltip: 'Wie heißt eure Meute, Sippe oder Roverrunde? Bitte mit dem dazugehörigem Präfix. '
              + '\n(Bitte achte auch auf die Rechtschreibung,'
              + ' da eine Korrektur aktuell nur durch einen Admin möglich ist.)',
          icon: 'mdi-group',
          fieldType: 'textfield',
          default: '',
          cols: 12,
        },
      ];
    },
  },
};
</script>
