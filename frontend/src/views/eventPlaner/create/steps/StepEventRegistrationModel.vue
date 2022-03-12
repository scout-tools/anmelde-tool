<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Bitte gib an wer sich wie registrieren kann.
            Können sich Stämme anmelden?
            Können sich Einzelpersonen anmelden?
            Müssen sich Stämme anmelden, bevor sich Einzelpersonen anmelden können?
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-card-text>
          <br>No = No single person registrations allowed
          <br>Attached = A single persons'
          registration has to be attached to a group registration
          <br>Mixed = A single persons'
          registration can be attached to a group registration but is not a must
          <br>External = Only standalone single persons' registrations allowed
        </v-card-text>
        <v-select
          v-model="singleChoice"
          :items="singleChoices"
          :error-messages="singleChoicesErrors"
          label="Model für Einzelanmeldungen auswählen"
          item-text="[1]"
          item-value="[0]"
          required
          @input="validate"
        />
      </v-row>
      <v-row align="center" justify="center">
        <v-card-text>
          <br>No = No group registration allowed
          <br>Optional = Group registration possible
          <br>Required = Group registration is required =>
          single registration can be only attached or not allowed at all
        </v-card-text>
        <v-select
          v-model="groupChoice"
          :items="groupChoices"
          :error-messages="groupChoicesErrors"
          label="Model für Gruppenanmeldungen auswählen"
          item-text="[1]"
          item-value="[0]"
          required
          @input="validate"
        />
      </v-row>
      <v-row align="center" justify="center">
        <v-card-text>
          Werden persönliche Daten benötigt?
        </v-card-text>
        <v-switch label="Persönliche Anmeldung" v-model="personalDataRequired"></v-switch>
      </v-row>
      <v-divider class="my-2"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import { mapGetters } from 'vuex';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';

export default {
  name: 'StepEventRegistrationModel',
  header: 'Registrierungsmodel',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    singleChoice: null,
    groupChoice: null,
    singleChoices: [],
    groupChoices: [],
    personalDataRequired: false,
  }),
  validations: {
    singleChoice: {
      required,
    },
    groupChoice: {
      required,
    },
  },
  computed: {
    singleChoicesErrors() {
      const errors = [];
      if (!this.$v.singleChoice.$dirty) return errors;
      if (!this.$v.singleChoice.required) {
        errors.push('Es muss ein Model ausgewählt werden.');
      }
      return errors;
    },
    groupChoicesErrors() {
      const errors = [];
      if (!this.$v.groupChoice.$dirty) return errors;
      if (!this.$v.groupChoice.required) {
        errors.push('Es muss ein Model ausgewählt werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    async getChoices() {
      this.loading = true;
      const urlGroupChoices = `${this.API_URL}/event/event-type-group-choices/`;
      const urlSingleChoices = `${this.API_URL}/event/event-type-single-choices/`;
      axios.all([
        axios.get(urlGroupChoices),
        axios.get(urlSingleChoices),
      ])
        .then(axios.spread((firstResponse, secondResponse) => {
          this.groupChoices = firstResponse.data;
          this.singleChoices = secondResponse.data;
        }))
        .catch((error) => {
          console.log(error);
          this.errorText = 'Fehler beim laden des Moduls';
          this.showError = true;
        });
    },
    updateData() {
      store.commit('createEvent/setRegistrationTypeGroup', this.singleChoice);
      store.commit('createEvent/setRegistrationTypeGroup', this.groupChoice);
      store.commit('createEvent/setPersonalDateRequired', this.personalDataRequired);
    },
  },
  created() {
    this.singleChoice = this.event.singleRegistration;
    this.groupChoice = this.event.groupRegistration;
    this.personalDataRequired = this.event.personalDataRequired;
    this.getChoices();
  },
};
</script>
