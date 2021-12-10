<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="pa-5 my-5">
      <v-row>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="myScoutname"
            readonly
            disabled
            filled
            :counter="20"
            label="Pfadfindername*"
            required
            @input="$v.data.scoutname.$touch()"
            @blur="$v.data.scoutname.$touch()"
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
                    'Gibt den Namen ein unter den die Person bekannt ' +
                    'ist, die den Workshop durchführt.'
                  }}
                </span>
              </v-tooltip>
            </template>
          </v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="data.firstname"
            :counter="20"
            :error-messages="firstnameErrors"
            label="Vorname*"
            required
            prepend-icon="mdi-card-account-details-outline"
            @input="$v.data.firstname.$touch()"
            @blur="$v.data.firstname.$touch()"
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
                    'Gib hier deinen Vornamen ein.'
                  }}
                </span>
              </v-tooltip>
            </template>
          </v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            v-model="data.lastname"
            :counter="20"
            :error-messages="lastnameErrors"
            label="Nachname*"
            required
            prepend-icon="mdi-card-account-details-outline"
            @input="$v.data.lastname.$touch()"
            @blur="$v.data.lastname.$touch()"
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
                    'Gib hier deinen Namenamen ein.'
                  }}
                </span>
              </v-tooltip>
            </template>
          </v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field readonly disabled filled :value="myBund" label="Bund">
          </v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field readonly disabled filled :value="myStamm" label="Stamm">
          </v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
          <v-text-field
            prepend-icon="mdi-at"
            :value="email"
            readonly
            disabled
            filled
            label="E-Mail"
          >
          </v-text-field>
        </v-col>
      </v-row>

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog ref="newLocationDialog" @close="getEvents()" />
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { minLength, required } from 'vuelidate/lib/validators';

import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvTextForStamm',
  displayName: 'Kontaktdaten',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    currentRegistration: [],
    data: {
      firstname: '',
      lastname: '',
    },
  }),
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'myStamm',
      'myBund',
      'myScoutname',
    ]),
    email() {
      return this.getJwtData.email;
    },

    firstnameErrors() {
      const errors = [];
      if (!this.$v.data.firstname.$dirty) return errors;
      if (!this.$v.data.firstname.required) {
        errors.push('Vorname ist erforderlich.');
      }
      if (!this.$v.data.firstname.minLength) {
        errors.push('Vorname muss mindestens 2 Zeichen lang sein.');
      }
      return errors;
    },
    lastnameErrors() {
      const errors = [];
      if (!this.$v.data.lastname.$dirty) return errors;
      if (!this.$v.data.lastname.required) {
        errors.push('Nachname ist erforderlich.');
      }
      if (!this.$v.data.lastname.minLength) {
        errors.push('Nachname muss mindestens 2 Zeichen lang sein.');
      }
      return errors;
    },
  },
  validations: {
    data: {
      firstname: {
        required,
        minLength: minLength(2),
      },
      lastname: {
        required,
        minLength: minLength(2),
      },
    },
  },
  watch: {
    currentRegistration() {
      if (this.currentRegistration && this.currentRegistration.length) {
        this.textfieldText = this.currentRegistration[0].freeText;
      }
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
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
      this.saveService();
    },
    beforeTabShow() {
      this.loadData();
    },
    async getRegistration() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${
          this.API_URL
        }basic/registration/?id=${registrationId}&timestamp=${new Date().getTime()}`,
      );
      return res.data;
    },
    loadData() {
      this.isLoading = true;
      Promise.all([this.getContact()])
        .then((values) => {
          if (values[0] && values[0].length) {
            this.data = values[0][0]; // eslint-disable-line
          }
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
    saveService() {
      this.data.registration = this.$route.params.id;
      this.data.scoutname = this.myScoutname;
      this.data.email = this.email;

      const { id } = this.data;

      if (id) {
        this.putContact(id).then(() => {
          this.$emit('nextStep');
        });
      } else {
        this.postContact().then(() => {
          this.$emit('nextStep');
        });
      }
    },
    async getContact() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${process.env.VUE_APP_API}/basic/contact/?registration=${registrationId}`,
      );
      return res.data;
    },
    async postContact() {
      const res = await axios.post(
        `${process.env.VUE_APP_API}/basic/contact/`,
        this.data,
      );
      return res.data;
    },
    async putContact(id) {
      const res = await axios.put(
        `${process.env.VUE_APP_API}/basic/contact/${id}/`,
        this.data,
      );
      return res.data;
    },
  },
};
</script>

<style>
</style>
