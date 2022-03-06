<template>
  <v-form ref="settingsUser">
    <v-container class="top-margin default-max-width mt-10">
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
                    Für diese Fahrt ist die Handynummer Pflicht. Falls du sie
                    nicht eintragen hast, kannst du sie nur unter den Profil
                    Einstellungen ändern.
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
        {{ 'Der Code ist falsch' }}
      </v-snackbar>
    </v-container>
  </v-form>
</template>

<script>
// import axios from 'axios';
import BaseField from '@/components/common/BaseField.vue';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { required, requiredIf } from 'vuelidate/lib/validators';

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
      data: {
        invitationCode: '',
        name: '',
        stamm: '',
        mobileNumber: '',
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
          tooltip: 'Name falsch? Ändern kannst du deinen Namen nur unter "Profil" (oben rechts)',
          icon: 'mdi-account-circle',
          fieldType: 'textfield',
          default: '',
          disabled: true,
          filled: true,
        },
        {
          name: 'Mein Stamm',
          techName: 'stamm',
          tooltip: 'Stamm falsch? Ändern kannst du deinen Stamm nur unter "Profil" (oben rechts)',
          icon: 'mdi-account-group',
          fieldType: 'textfield',
          default: '',
          disabled: true,
          filled: true,
        },
        {
          name: 'Telefonnummer',
          techName: 'mobileNumber',
          tooltip: 'Telefonnummer fehlt oder ist falsch? Hinzufügen kannst du deine Nummer nur unter "Profil" (oben rechts)',
          icon: 'mdi-phone',
          mandatory: true,
          fieldType: 'textfield',
          default: '',
        },
      ],
    };
  },
  validations: {
    data: {
      invitationCode: {
        required,
      },
      mobileNumber: {
        required: requiredIf(() => true),
      },
    },
  },
  props: ['scoutOrganisation'],
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
    // mobileNumber() {
    //   return this.items.mobileNumber;
    // },
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
    // getCodeParam() {
    //   if (this.invitationCode) {
    //     return this.invitationCode;
    //   }
    //   return '';
    // },
    // invitationCodeErrors() {
    //   const errors = [];
    //   if (!this.$v.invitationCode.$dirty) return errors;
    //   // eslint-disable-next-line
    //   !this.$v.invitationCode.required &&
    //     errors.push('Der Einladungscode wird benötigt');
    //   return errors;
    // },
    // mobileNumberErrors() {
    //   const errors = [];
    //   if (!this.$v.mobileNumber.$dirty) return errors;
    //   // eslint-disable-next-line
    //   !this.$v.mobileNumber.required &&
    //     errors.push(
    //       'Telefonnummer ist für diese Fahrt verpflichtend.
    // Wechsele ins Profil um die Telefonnummer hinzuzufügen',
    //     );
    //   return errors;
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
    },

    createRegestration() {
      // TODO: implement
      // axios
      //   .post(`${this.API_URL}basic/registration/?code=${this.getCodeParam}`, {
      //     responsiblePersons: [this.getJwtData.email],
      //     scoutOrganisation: this.items.scoutOrganisation,
      //     event: this.eventId,
      //   })
      //   .then((response) => {
      //     this.$router.push({
      //       name: 'registrationCreate',
      //       params: {
      //         id: response.data.id,
      //         event: response.data.event,
      //         scoutOrganisation: this.items.scoutOrganisation,
      //       },
      //     });
      //   })
      //   .catch(() => {
      //     this.showError = true;
      //     console.log('Fehler');
      //   });
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
