<template>
  <v-form ref="formNameDescription" v-model="valid">
        <v-card flat>
          <travel-picker
            title="Mosaikersleben"
          />
        </v-card>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import TravelPicker from '../components/TravelPicker.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Abreise',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
    TravelPicker,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      maxNumber: 25,
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
      this.$emit('nextStep');
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
