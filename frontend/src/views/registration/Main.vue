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
                  <!-- <v-subheader class="ma-0">
                    <v-icon class="ma-2" color="error"
                      >mdi-alert-circle
                    </v-icon>
                    Für diese Fahrt ist die Handynummer Pflicht. Falls du sie
                    nicht eintragen hast, kannst du sie nur unter den Profil
                    Einstellungen ändern.
                  </v-subheader> -->
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
                        color="secondary"
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

export default {
  mixins: [validationMixin],
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
      data: {
        invitationCode: '',
        name: '',
        stamm: '',
        mobileNumber: '',
        single: false,
      },
      fields: [
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
          name: 'Einzel/Gruppen Anmeldung',
          techName: 'single',
          tooltip: 'Meldest du dich oder deinen Stamm an?',
          icon: 'mdi-account-group',
          fieldType: 'radio',
          referenceTable: [
            {
              name: 'Stammesanmeldung',
              value: false,
            },
            {
              name: 'Einzelanmeldung',
              value: true,
            },
          ],
        },
      ],
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
      // mobileNumber: {
      //   required: requiredIf(() => true),
      // },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    eventId() {
      return this.$route.params.id;
    },
    // isMobilMandatory() {
    //   if (this.event) {
    //     return false;
    //     // return this.event.eventTags.filter((tag) => tag === 1).length;
    //   }
    //   return false;
    // },
    mobileNumber() {
      return this.personalData.mobileNumber;
    },
    // getItems() {
    //   return this.items;
    // },

    // email() {
    //   return this.getJwtData.email;
    // },
    // getStammName() {
    //   const obj = this.hierarchyMapping.find(
    //     (user) => user.id === this.items.scoutOrganisation,
    //   );
    //   if (obj && obj.name) {
    //     return obj.name;
    //   }
    //   return 'Kein Stamm';
    // },
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
      this.data.stamm = this.userinfo.stamm;
      this.data.name = this.userinfo.name;

      this.loadUserData();
    },

    loadUserData() {
      this.loading = true;
      const path = `${this.API_URL}/auth/personal-data/`;
      axios
        .get(path)
        .then((res) => {
          this.data.mobileNumber = res.data.mobileNumber;
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

<style scoped>
.default-max-width {
  max-width: 800px !important;
}
</style>
