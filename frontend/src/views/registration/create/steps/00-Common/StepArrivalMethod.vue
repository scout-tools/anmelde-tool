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
      <p>Wie werdet ihr anreisen?</p>
      <v-row>
        <v-col cols="4" sm="8">
          <v-btn-toggle
            v-model="data.vehicle"
            tile
            color="blue accent-3"
            group
            multiple
          >
            <v-btn value="tain"> Bahn </v-btn>

            <v-btn value="bus"> Reisebus </v-btn>
            <v-btn value="car"> PKW </v-btn>
            <v-btn value="else"> Sonstiges </v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('car')"
            label="Wieviele PKWs?"
          >
          </v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('else')"
            label="Sonstiges Vekehrsmittel"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <p
          class="text-center"
          v-if="data.vehicle.includes('car')"
          style="border-style: solid; border-color: red"
        >
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-spin
          </v-icon>
          Bitte beachtet, dass vor Ort selbst nur sehr wenige bis keine
          Parkplätze zur Verfügung stehen und PKW daher ggf. in einiger
          Entfernung im Umland abgestellt werden müssen.
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-flip-h mdi-spin
          </v-icon>
        </p>
        <p
          class="text-center"
          v-if="!data.vehicle.includes('car')"
          style="border-style: solid; border-color: green"
        >
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline
          </v-icon>
          Mega Cool, dass ihr ohne Auto anreist.
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline mdi-flip-h
          </v-icon>
        </p>
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
  name: 'StepArrivalMethod',
  displayName: 'Anreise-Methode',
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
