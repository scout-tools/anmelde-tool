<template>
  <v-form v-model="valid">
    <v-container>
      <v-row class="mt-2" center>
        <span class="text-center ma-5 subtitle-1">
          <p>
            Weitere Informationen zu An- und Abreise findet ihr auf
            <a href="https://www.bundesfahrt.de" target="_blank"
              >www.bundesfahrt.de</a
            >.
            Bitte teile uns mit, wie viele Teilnehmer_innen jeweils auf welche
            Art zur Kaperfahrt anreisen.
          </p>
        </span>
      </v-row>
      <v-card flat>
        <travel-picker
          ref="kaperfahrtTravelpicker"
          :travelTag="this.travelTag"
          :participantRole="this.participantRole"
          title="Kaperfahrt / Bundesmeutenlager"
        />
      </v-card>
      <p v-if="this.errorNotFinished" style="color:red">
        Verteile alle deine Teilnehmer!
      </p>
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
  name: 'StepTravel',
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
    participantRole: [6],
    items: [],
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
      if (this.$refs.kaperfahrtTravelpicker) {
        if (this.$refs.kaperfahrtTravelpicker.done) {
          const methodOfTravel = this.$refs.kaperfahrtTravelpicker.getData();

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
      if (this.$refs.kaperfahrtTravelpicker
      ) {
        this.$refs.kaperfahrtTravelpicker.refresh();
      }
    },
  },
};
</script>
