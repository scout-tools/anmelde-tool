<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Bitte gib an wer sich wie registrieren kann.
            Können sich Stämme anmelden?
            Können sich Einzelpersonen anmelden?
            Müssen sich Stämme anmelden, bevor sich Einzelpersonen anmelden können?
          <br/>
           Wähle dazu einfach aus der Liste die entsprechende IDM Gruppe aus.
          <br/>
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-select
          v-model="choice"
          :items="choices"
          :error-messages="choicesErrors"
          label="Model auswählen "
          item-text="[1]"
          item-value="[0]"
          required

          @input="validate"
        />
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
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
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
    choice: null,
    choices: [],
  }),
  validations: {
    choice: {
      required,
    },
  },
  computed: {
    choicesErrors() {
      const errors = [];
      if (!this.$v.choice.$dirty) return errors;
      if (!this.$v.choice.required) {
        errors.push('Es muss mindestens eine Gruppe ausgewählt werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    async getChoices() {
      const url = `${this.API_URL}/event/event-type-choices/`;
      axios.get(url)
        .then((success) => {
          this.choices = success.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    updateData() {
      console.log(this.choice);
      store.commit('createEvent/setRegistrationModel', this.choice);
    },
  },
  created() {
    this.choice = this.event.registrationModel;
    this.getChoices();
  },
};
</script>
