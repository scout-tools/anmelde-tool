<template>
  <v-container fluid style="width:70%">
    <v-form v-model="valid">
      <v-card flat v-if="!isLoading">
        <v-row align="center">
          <v-col cols="12">
            <v-card-text>
              {{this.reached()}} / {{this.data.maxNumber}}
              <v-icon v-if="this.reached() === this.data.maxNumber">mdi-check</v-icon>
            </v-card-text>
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col cols="6">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 1)[0].numberOfPersons"
              label="Bus"
              required
              prepend-icon="mdi-bus"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 2)[0].numberOfPersons"
              label="PKW"
              required
              prepend-icon="mdi-car"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 3)[0].numberOfPersons"
              label="OEPNV"
              required
              prepend-icon="mdi-bus-stop"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 4)[0].numberOfPersons"
              label="zu Fuss"
              required
              prepend-icon="mdi-hiking"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 5)[0].numberOfPersons"
              label="Wasserweg"
              required
              prepend-icon="mdi-ship-wheel"
            />
          </v-col>
          <v-col cols="6" v-if="this.travelTag === 3">
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 6)[0].numberOfPersons"
              label="Lunchpaket"
              required
              prepend-icon="mdi-food-apple"
            />
          </v-col>
          <v-col cols="6" v-else>
            <v-text-field
              v-model="data.methodOfTravels.filter((i) => i.travelType === 7)[0].numberOfPersons"
              label="Schon da"
              required
              prepend-icon="mdi-account-check"
            />
          </v-col>
        </v-row>
      </v-card>
      <v-card v-else>
        <div class="text-center ma-5">
          <v-progress-circular
            :size="80"
            :width="10"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>
      </v-card>
    </v-form>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import axios from 'axios';

export default {
  props: ['title', 'travelTag', 'participantRole'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      maxNumber: 0,
      numberAlreadyThere: 0,
      methodOfTravels: [
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 1, // Reisebus
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 2, // PKW
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 3, // OEPNV
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 4, // zu fuss
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 5, // Wasserweg
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 6, // Lunchpaket
          travelTag: -1,
        },
        {
          numberOfPersons: 0,
          registration: 0,
          travelType: 7, // Schon da
          travelTag: -1,
        },
      ],
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
  mounted() {
    this.loadData();
  },
  methods: {
    loadData() {
      this.isLoading = true;
      Promise.all([this.getMaxNumber(), this.getMethod()])
        .then((values) => {
          this.participantRole.forEach((j) => {
            this.data.maxNumber += values[0][0].participantpersonalSet.filter(
              (i) => i.participantRole === j,
            ).length;
          });
          const list = values[1].filter((i) => i.travelTag === this.travelTag);
          if (list.length > 0) {
            this.data.methodOfTravels = list;
          }
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
    async getMethod() {
      const res = await axios.get(`${this.API_URL}basic/method-of-travel/`);
      return res.data;
    },
    reached() {
      let sum = 0;
      this.data.methodOfTravels.forEach((i) => {
        sum += i.numberOfPersons * 1;
      });
      sum += this.data.numberAlreadyThere;
      return sum;
    },
    async getMaxNumber() {
      const path = `${process.env.VUE_APP_API}basic/registration/`;
      const answer = await axios.get(
        `${path}${
          this.$route.params.id
        }/participants/?&timestamp=${new Date().getTime()}`,
      );
      return answer.data;
    },
    getData() {
      return this.data.methodOfTravels;
    },
  },
};
</script>
