<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-form>
        <p>
          Gib hier eine Adresse innerhalb Deutschlands an, wo wir ein
          Überraschungspaket für deinen Stamm hinschicken können.
        </p>

        <v-divider class="my-2" />
        <v-subheader> Adresse </v-subheader>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.firstName"
              :counter="20"
              :error-messages="firstNameErrors"
              label="Vorname*"
              required
              prepend-icon="mdi-card-account-details-outline"
              @input="$v.data.firstName.$touch()"
              @blur="$v.data.firstName.$touch()"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Trag bitte den Vornamen des_der Teilnehmer_in ' +
                      'ein. Zweitnamen müssen nicht mit angegeben werden.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.lastName"
              :counter="20"
              :error-messages="lastNameErrors"
              label="Nachname*"
              required
              prepend-icon="mdi-card-account-details-outline"
              @input="$v.data.lastName.$touch()"
              @blur="$v.data.lastName.$touch()"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ 'Trag bitte den vollständigen Nachnamen ein.' }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.street"
              :counter="40"
              :error-messages="streetErrors"
              label="Straße und Hausnummer*"
              prepend-icon="mdi-home"
              required
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ 'Trag bitte Straße und Hausnummer ein.' }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="data.addressAddition"
              :counter="40"
              :error-messages="addressAdditionErrors"
              label="Adresszusatz"
              prepend-icon="mdi-home"
              placeholder="Freiwllig"
              required
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ 'Trag bitte den Adresszusatz ein.' }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-autocomplete
              v-model="data.zipCode"
              :items="zipCodeMapping"
              :item-text="customText"
              required
              :error-messages="zipCodeErrors"
              item-value="id"
              label="Stadt / Postleitzahl*"
              placeholder="Wähle Stadt oder Postleitzahl"
              prepend-icon="mdi-city"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{
                      'Trage bitte den Wohnort oder die Postleitzahl ' +
                      'des Wohnorts ein und wähle die richtige Option aus.'
                    }}
                  </span>
                </v-tooltip>
              </template>
            </v-autocomplete>
          </v-col>
        </v-row>
      </v-form>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="onCloseWindow()" />
  </v-form>
</template>

<script>
import { required, minLength, maxLength } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Paketadresse',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    radioGroup: 0,
    radioGroup2: 0,
    data: {
      firstName: null,
      lastName: null,
      street: null,
      addressAddition: null,
      zipCode: null,
    },
  }),
  validations: {
    data: {
      firstName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      lastName: {
        required,
        minLength: minLength(2),
        maxLength: maxLength(20),
      },
      street: {
        required,
        minLength: minLength(5),
        maxLength: maxLength(30),
      },
      zipCode: {
        required,
        minLength: minLength(1),
      },
      addressAddition: {
        minLength: minLength(2),
        maxLength: maxLength(30),
      },
    },
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'zipCodeMapping',
    ]),
    firstNameErrors() {
      const errors = [];
      if (!this.$v.data.firstName.$dirty) return errors;
      if (!this.$v.data.firstName.required) {
        errors.push('Vorname ist erforderlich.');
      }
      if (!this.$v.data.firstName.minLength) {
        errors.push('Vorname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.firstName.maxLength) {
        errors.push('Vorname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    lastNameErrors() {
      const errors = [];
      if (!this.$v.data.lastName.$dirty) return errors;
      if (!this.$v.data.lastName.required) {
        errors.push('Nachname ist erforderlich.');
      }
      if (!this.$v.data.lastName.minLength) {
        errors.push('Nachname muss mindestens 2 Zeichen lang sein.');
      }
      if (!this.$v.data.lastName.maxLength) {
        errors.push('Nachname darf maximal 20 Zeichen lang sein.');
      }
      return errors;
    },
    streetErrors() {
      const errors = [];
      if (!this.$v.data.street.$dirty) return errors;
      if (!this.$v.data.street.required) {
        errors.push('Adresse ist erforderlich.');
      }
      if (!this.$v.data.street.minLength) {
        errors.push('Adresse muss mindestens 5 Zeichen lang sein.');
      }
      if (!this.$v.data.street.maxLength) {
        errors.push('Adresse darf maximal 30 Zeichen lang sein.');
      }
      return errors;
    },
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.data.zipCode.$dirty) return errors;

      if (!this.$v.data.zipCode.minLength) {
        errors.push('Stadt ist erforderlich.');
      }

      if (!this.$v.data.zipCode.required) {
        errors.push('Stadt ist erforderlich.');
      }
      return errors;
    },
    addressAdditionErrors() {
      const errors = [];
      if (!this.$v.data.addressAddition.$dirty) return errors;

      // eslint-disable-next-line
      !this.$v.data.addressAddition.maxLength &&
        errors.push('Darf nicht mehr als 20 Zeichen haben');
      return errors;
    },
  },
  watch: {
    radioGroup(value) {
      this.$store.commit('setDpvAddedLocation', value === '1');
    },
  },
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      // this.$store.commit('setDpvAddedLocation', true);
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
    beforeTabShow() {},
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
