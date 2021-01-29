<template>
  <v-form ref="settingsUser">
    <v-container class="top-margin">
      <v-row justify="center">
        <v-flex ma-3 lg9>
          <v-layout column>
            <v-card>
              <v-card-title class="text-center justify-center py-6">
                Deine persönlichen Daten
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-subheader class="ma-5">
                    Bitte füge folgende Daten in dein Profil hinzu, damit
                    das Anmelde-Tool in der Lage ist, dich korrekt zuzuordnen. <br>
                    Diese Daten sind für nur für die
                    Lagerleitung nach deiner explizieten Anmeldung zu einem Lager sichtbar.
                  </v-subheader>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="invitationCode"
                        label="Code aus der Einladung"
                        counter="6"
                        prepend-icon="mdi-lock"
                        :error-messages="invitationCodeErrors"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.invitationCode }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        readonly
                        filled
                        v-model="items.scoutName"
                        label="Mein Name"
                        prepend-icon="mdi-account-circle"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.scoutName }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        readonly
                        filled
                        v-model="getStammName"
                        label="Mein Stamm"
                        prepend-icon="mdi-account-group"
                      >
                        <template slot="append">
                          <v-tooltip bottom>
                            <template v-slot:activator="{ on, attrs }">
                              <v-icon
                                color="success"
                                dark
                                v-bind="attrs"
                                v-on="on"
                              >
                                mdi-help-circle-outline
                              </v-icon>
                            </template>
                            <span>
                              {{ tooltip.stammName }}
                            </span>
                          </v-tooltip>
                        </template>
                      </v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-btn color="success" @click="onSaveClicked">
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
import axios from 'axios';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { required } from 'vuelidate/lib/validators';

export default {
  mixins: [validationMixin],

  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      invitationCode: '',
      scoutName: '',
      reg_id: null,
      showError: false,
      items: {},
      tooltip: {
        email: '123',
        scoutName: '456',
        invitationCode:
          'Hast du keinen Code bekommen? Gucke nochmal in der Einladung.'
          + 'Falls du nichts findest melde dich bei der Lagerleitung, deiner Bundesführung oder bei support@anmelde-too.de',
      },
    };
  },
  validations: {
    invitationCode: {
      required,
    },
  },
  props: ['scoutOrganisation'],
  computed: {
    getItems() {
      return this.items;
    },
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping']),
    email() {
      return this.getJwtData.email;
    },
    getStammName() {
      const obj = this.hierarchyMapping.find(
        (user) => user.id === this.items.scoutOrganisation,
      );
      if (obj && obj.name) {
        return obj.name;
      }
      return 'Kein Stamm';
    },
    getCodeParam() {
      if (this.invitationCode) {
        return this.invitationCode;
      }
      return '';
    },
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.invitationCode.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.invitationCode.required &&
        errors.push('Der Einladungscode wurd benötigt');
      return errors;
    },
  },
  methods: {
    tranferId(id) {
      this.items.scoutOrganisation = id;
    },
    onPickStammClick() {
      this.$refs.pickStamm.show(this.items.scoutOrganisation);
    },
    onSaveClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createRegestration();
    },
    getData() {
      this.loadUserExtended();
    },
    loadUserExtended() {
      const path = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    createRegestration() {
      const eventId = this.$route.params.id;
      axios
        .post(`${this.API_URL}basic/registration/?code=${this.getCodeParam}`, {
          responsiblePersons: [this.getJwtData.email],
          scoutOrganisation: this.items.scoutOrganisation,
          event: eventId,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationCreate',
            params: {
              id: response.data.id,
              event: response.data.event,
              scoutOrganisation: this.items.scoutOrganisation,
            },
          });
        })
        .catch(() => {
          this.showError = true;
          console.log('Fehler');
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
