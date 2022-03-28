<template>
  <v-form ref="settingsUser">
    <v-container class="top-margin default-max-width">
      <v-row justify="center">
        <v-flex ma-3 lg9>
          <v-layout column>
            <v-card>
              <v-card-title class="text-center justify-center py-6">
                Anmeldung starten
              </v-card-title>
              <v-card-text>
                <v-container>
                  <div class="ma-2">
                    <p class="ma-0">
                      Hast du keinen Code bekommen? Schaue nochmal in der
                      Einladung. Falls du nichts findest, melde dich beim
                      Veranstalter, deiner Bundesführung oder bei:
                      <a href="mailto:support@anmelde-tool.de"
                        >support@anmelde-tool.de</a
                      >
                    </p>
                    <p class="mt-4">
                      Bevor deine Anmeldung verbindlich ist, musst du sie im
                      letzten Schritt ausdrücklich bestätigen. Du kannst deinen
                      Anmeldevorgang zu jedem Zeitpunkt abbrechen und später
                      fortsetzen. Deine Daten kannst du bis zum Anmeldeschluss
                      verändern.
                    </p>
                  </div>
                  <v-subheader class="ma-0">
                    <v-icon class="ma-2" color="error"
                      >mdi-alert-circle
                    </v-icon>
                    Für diese Fahrt ist die Handynummer Pflicht. Bitte im Profil hinzufügen.
                  </v-subheader>
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
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-btn
                        color="primary"
                        @click="onCreateRegistrationClicked"
                      >
                        <v-icon left dark>mdi-check</v-icon>
                        Anmeldung starten
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-actions>
            </v-card>
          </v-layout>
        </v-flex>
      </v-row>
      <v-snackbar v-model="showError" color="error" y="top">
        {{ errorMessage }}
      </v-snackbar>
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import BaseField from '@/components/common/BaseField.vue';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { required } from 'vuelidate/lib/validators';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [validationMixin, apiCallsMixin],
  components: {
    BaseField,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      showError: false,
      errorMessage: 'Fehler',
      personalData: {},
      currentEvent: {},
      data: {
        invitationCode: '',
        name: '',
        stamm: '',
        mobileNumber: '',
        single: false,
      },
    };
  },
  validations: {
    data: {
      invitationCode: {
        required,
      },
      single: {
        required,
      },
      mobileNumber: {
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
          cols: 7,
        },
        {
          name: 'Mein Name',
          techName: 'name',
          tooltip:
            'Name falsch? Ändern kannst du deinen Namen nur unter "Profil" (oben rechts)',
          icon: 'mdi-account-circle',
          fieldType: 'textfield',
          default: '',
          disabled: true,
          filled: true,
        },
        {
          name: 'Mein Stamm',
          techName: 'stamm',
          tooltip:
            'Stamm falsch? Ändern kannst du deinen Stamm nur unter "Profil" (oben rechts)',
          icon: 'mdi-account-group',
          fieldType: 'textfield',
          default: '',
          disabled: true,
          filled: true,
        },
        {
          name: 'Telefonnummer',
          techName: 'mobileNumber',
          tooltip: '',
          icon: 'mdi-phone',
          fieldType: 'textfield',
          default: '',
          disabled: true,
          filled: true,
        },
        {
          name: 'Einzel/Gruppen Anmeldung',
          techName: 'single',
          tooltip: 'Meldest du dich oder deinen Stamm an?',
          icon: 'mdi-account-group',
          fieldType: 'radio',
          referenceTable: this.getGroupRefTable,
          cols: 12,
        },
      ];
    },
    ...mapGetters(['userinfo']),
    eventId() {
      return this.$route.params.id;
    },
    getGroupRefTable() {
      const returnArray = [];
      if (this.currentEvent.singleRegistration !== 'N') {
        returnArray.push({
          name: 'Einzelanmeldung',
          value: true,
        });
      }
      if (this.currentEvent.groupRegistration !== 'N') {
        returnArray.push({
          name: 'Stammesanmeldung',
          value: false,
        });
      }
      return returnArray;
    },
  },
  methods: {
    onCreateRegistrationClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createRegestration();
    },
    setData() {
      this.data.name = this.userinfo.name;

      this.loadData();
    },

    loadData() {
      this.loading = true;
      Promise.all([this.getPersonalData(), this.getEvent(this.eventId)])
        .then((values) => {
          this.data.mobileNumber = values[0].data.mobileNumber; //eslint-disable-line
          this.currentEvent = values[1].data; //eslint-disable-line
          this.data.stamm = values[0].data.scoutOrganisation.name; //eslint-disable-line
          this.loading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
    createRegestration() {
      axios
        .post(`${this.API_URL}/event/registration/`, {
          eventCode: this.data.invitationCode,
          event: this.eventId,
          single: this.data.single,
        })
        .then((response) => {
          console.log(response.data.id);
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
  created() {
    this.setData();
  },
};
</script>

<style>
.default-max-width {
  max-width: 800px !important;
}
</style>
