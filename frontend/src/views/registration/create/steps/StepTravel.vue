<template>
  <v-form ref="formNameDescription" v-model="valid">
        <v-card flat>
          <travel-picker
            :input=this.getMethod
            title="Kaperfahrt"
            @save="saveTravel"></travel-picker>
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
import axios from 'axios';
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import TravelPicker from '../components/TravelPicker.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Anreise - Kaperfahrt',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
    TravelPicker,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    travelTag: 1,
    items: [],
    filteredItems: [],
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
  created() {

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
    getMethod() {
      axios
        .get(
          `${this.API_URL}basic/method-of-travel/`,
        )
        .then((res) => res.data.filter((i) => i.travelTag === this.travelTag))
        .catch((err) => {
          console.log(err);
        });
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
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    saveTravel(methodOfTravel) {
      methodOfTravel.forEach((i) => {
        // eslint-disable-next-line no-param-reassign
        i.registration = parseInt(this.$route.params.id, 10);
        // eslint-disable-next-line no-param-reassign
        i.travelTag = this.travelTag;
      });
      console.log(methodOfTravel);

      const promises = [];
      const myUrl = `${this.API_URL}basic/method-of-travel/`;
      methodOfTravel.forEach((i) => {
        promises.push(axios.post(myUrl, i));
      });
      Promise.all(promises).then(() => {
        this.$emit('nextStep');
      });
    },
  },
};
</script>
