<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container fluid>
      <v-row align="center">
        <v-col cols="6">
          <v-subheader>
            {{this.reached()}} / {{this.data.maxNumber}}
          </v-subheader>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col cols="6">
          <v-text-field
            v-model="data.numberBus"
            :error-messages="numberError"
            label="Bus"
            required
            @input="$v.data.numberBus.$touch()"
            @blur="$v.data.numberBus.$touch()"
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="data.numberCar"
            :error-messages="numberError"
            label="PKW"
            required
            @input="$v.data.numberCar.$touch()"
            @blur="$v.data.numberCar.$touch()"
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="data.numberPublic"
            :error-messages="numberError"
            label="OEPNV"
            required
            @input="$v.data.numberPublic.$touch()"
            @blur="$v.data.numberPublic.$touch()"
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="data.numberWalking"
            :error-messages="numberError"
            label="zu Fuss"
            required
            @input="$v.data.numberWalking.$touch()"
            @blur="$v.data.numberWalking.$touch()"
          />
        </v-col>
        <v-col cols="6">
          <v-text-field
            v-model="data.numberWater"
            :error-messages="numberError"
            label="Wasserweg"
            required
            @input="$v.data.numberWater.$touch()"
            @blur="$v.data.numberWater.$touch()"
          />
        </v-col>
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
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Anreise',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      maxNumber: 0,
      numberBus: 0,
      numberCar: 0,
      numberPublic: 0,
      numberWalking: 0,
      numberWater: 0,
    },
  }),
  validations: {
    data: {
      required,
      minLength: minLength(1),
      $each: {
        minValue: minValue(1),
      },
    },
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping', 'ageGroupMapping']),
    total() {
      return Object.values(this.data).reduce((pv, cv) => parseInt(pv, 10) + parseInt(cv, 10), 0);
    },
    mobileNumberErrors() {
      const errors = [];
      if (!this.$v.mobileNumber.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.mobileNumber.maxLength &&
        errors.push('Name must be at most 10 characters long');
      // eslint-disable-next-line
      !this.$v.mobileNumber.minLength &&
        errors.push('Name must be at most 10 characters long');
      return errors;
    },
  },
  methods: {
    reached() {
      // eslint-disable-next-line max-len
      const sum = this.data.numberBus * 1 + this.data.numberCar * 1 + this.data.numberPublic * 1 + this.data.numberWalking * 1 + this.data.numberWater * 1;
      return sum;
    },
    greaterThanZero(value) {
      return value > 0;
    },
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

      this.addParticipants();
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
