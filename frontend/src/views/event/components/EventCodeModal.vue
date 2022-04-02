<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Einladungscode</v-card-title>
          <v-card-text>
            <div class="ma-2">
              <p class="ma-0">
                Hast du keinen Code bekommen? Schaue nochmal in der Einladung.
                Falls du nichts findest, melde dich beim Veranstalter, deiner
                Bundesführung oder bei:
                <a href="mailto:support@anmelde-tool.de"
                  >support@anmelde-tool.de</a
                >
              </p>
              <p class="mt-4">
                Bevor deine Anmeldung verbindlich ist, musst du sie im letzten
                Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang
                zu jedem Zeitpunkt abbrechen und später fortsetzen. Deine Daten
                kannst du bis zum Anmeldeschluss verändern.
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
                  />
                </template>
              </v-row>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="grey darken-1" text @click="cancel()"> Zurück </v-btn>
            <v-btn color="success" text @click="onDeleteClicked">
              Anmeldung starten
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
    timeout: 3000,
    data: {},
  }),
  components: {
    BaseField,
  },
  mixins: [apiCallsMixin],
  methods: {
    onDeleteClicked() {
      this.onCreateRegistrationClicked();
    },
    show(item, single) {
      this.single = single;
      this.item = item;
      this.dialog = true;
    },

    cancel() {
      this.dialog = false;
    },
    onCreateRegistrationClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createRegestration();
    },
    createRegestration() {
      axios
        .post(`${this.API_URL}/event/registration/`, {
          eventCode: this.data.invitationCode,
          event: this.item.id,
          single: this.single,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationEdit',
            params: {
              id: response.data.id,
            },
          });
        })
        .catch((error) => {
          console.log(error);
          this.showError = true;
          this.errorMessage = error.response.data.detail;
        });
    },
  },
  validations: {
    data: {
      invitationCode: {
        required,
      },
    },
  },
  computed: {
    fields() {
      return [
        {
          name: 'Code aus der Einladung',
          techName: 'invitationCode',
          tooltip: 'Der Code steht in der offizellen Anmeldung.',
          icon: 'mdi-lock',
          fieldType: 'textfield',
          default: '',
          cols: 12,
        },
      ];
    },
  },
};
</script>
