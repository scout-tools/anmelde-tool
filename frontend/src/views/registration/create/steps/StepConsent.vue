<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p>
            Ich möchte mich zur <b>{{ currentEvent.name }}</b> anmelden. <br />
            <br />

            Ich melde hiermit folgende Organsition <b> {{ myStamm }} </b> an.
            <br />
            <br />

            Ich bin zukünfig der Ansprechpartner und bin unter meiner E-Mail
            Adresse: <br />
            <br />
            <b>{{ myEmail }} </b> <br />
            <br />
            zu erreichen.
          </p>
        </span>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox v-model="data.checkbox1" :label="`Ich Stimme zu`">
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';

import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Einverständnis',
  props: ['position', 'maxPos', 'currentEvent', 'currentRegistration', 'scoutOrganisation'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      checkbox1: false,
      name: '',
      description: '',
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'hierarchyMapping', 'getJwtData']),
    myStamm() {
      if (this.scoutOrganisation) {
        return this.hierarchyMapping.find(
          (user) => user.id === this.scoutOrganisation,
        ).name;
      }
      return 'Keine Name';
    },
    myEmail() {
      return this.getJwtData.email;
    },
  },
  methods: {
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
  },
};
</script>
