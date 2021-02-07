<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
    <v-row class="mt-2" center>
        <span class="text-center ma-5 subtitle-1">
          <p>
            Informationen zu An- und Abreise findet ihr auf
            <a href="https://www.bundesfahrt.de" target="_blank">www.bundesfahrt.de</a>.
          </p>
        </span>
    </v-row>
    <v-card flat>
      <travel-picker
        ref="backTravelpicker"
        :travelTag=this.travelTag
        :participantRole=this.participantRole
        title="Kaperfahrt / Bundesmeutenlager"
      />
    </v-card>
    <v-divider class="my-3" />
    <prev-next-buttons
      :position="position"
      :max-pos="maxPos"
      @nextStep="nextStep"
      @prevStep="prevStep"
    />
  </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import TravelPicker from '../components/TravelPicker.vue';

export default {
  name: 'StepTravelBack',
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
    travelTag: 3,
    participantRole: [5, 6],
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
      this.onSaveTravelHandler();
    },
    onSaveTravelHandler() {
      if (this.$refs.backTravelpicker) {
        const methodOfTravel = this.$refs.backTravelpicker.getData();

        if (!methodOfTravel[0].id || methodOfTravel[0].id === 0) {
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
        } else {
          const promises = [];
          methodOfTravel.forEach((i) => {
            promises.push(axios.put(`${this.API_URL}basic/method-of-travel/${i.id}/`, i));
          });
          Promise.all(promises).then(() => {
            this.$emit('nextStep');
          });
        }
      }
    },
    beforeTabShow() {
    },
  },
};
</script>
