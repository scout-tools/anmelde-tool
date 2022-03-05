<template>
  <v-form v-model="valid">
    <v-container>
      <!-- <v-row class="mt-2" center>
        <span class="text-center ma-5 subtitle-1">
          <p>
            Wie werdet ihr anreisen?
          </p>
        </span>
      </v-row> -->
      <p>Wann werdet ihr anreisen?</p>
      <v-row>
        <v-col cols="12" class="py-2">
          <p>Wann werdet ihr voraussichtlich an ankommen?</p>

          <v-btn-toggle v-model="data.time" tile color="blue accent-3" group>
            <v-btn value="left"> 16:00 - 18:00</v-btn>

            <v-btn value="center"> 18:00 - 20:00</v-btn>
            <v-btn value="right"> 20:00 - 22:00 </v-btn>
            <v-btn value="123"> 22:00 - 0:00 </v-btn>
            <v-btn value="later"> Noch Später</v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="3">
          <v-text-field v-show="data.time.includes('later')" label="Wann etwa?">
          </v-text-field>
        </v-col>
      </v-row>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep(true)"
        @prevStep="prevStep"
      />
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import { stepMixin } from '@/mixins/stepMixin'; // eslint-disable-line
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepArrivalTime',
  displayName: 'Anreise-Zeit',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    travelTag: 1,
    participantRole: [6],
    data: {
      vehicle: [],
      time: [],
    },
    filteredItems: [],
    errorNotFinished: false,
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
  created() {},
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'ageGroupMapping',
    ]),
    total() {
      return Object.values(this.data).reduce(
        (pv, cv) => parseInt(pv, 10) + parseInt(cv, 10),
        0,
      );
    },
  },
  methods: {
    greaterThanZero(value) {
      return value > 0;
    },
    onSaveTravelHandler() {
      if (this.$refs.kaperfahrtTravelpicker) {
        this.$refs.kaperfahrtTravelpicker.resetNull();
        if (this.$refs.kaperfahrtTravelpicker.done) {
          const methodOfTravel = this.$refs.kaperfahrtTravelpicker.getData();

          if (!methodOfTravel[0].id || methodOfTravel[0].id === 0) {
            methodOfTravel.forEach((i) => {
              // eslint-disable-next-line no-param-reassign
              i.registration = parseInt(this.$route.params.id, 10);
              // eslint-disable-next-line no-param-reassign
              i.travelTag = this.travelTag;
            });

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
              promises.push(
                axios.put(`${this.API_URL}basic/method-of-travel/${i.id}/`, i),
              );
            });
            Promise.all(promises).then(() => {
              this.$emit('nextStep');
            });
          }
        } else {
          this.errorNotFinished = true;
        }
      }
    },
    beforeTabShow() {
      if (this.$refs.kaperfahrtTravelpicker) {
        this.$refs.kaperfahrtTravelpicker.refresh();
      }
      this.errorNotFinished = false;
    },
  },
};
</script>
