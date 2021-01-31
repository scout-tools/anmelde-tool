<template>
  <v-container fluid style="width:70%">
    <v-form v-model="valid">
      <v-card flat>
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
          <v-col cols="6">
            <v-text-field
              v-model="data.numberAlreadyThere"
              label="Schon da"
              required
              prepend-icon="mdi-account-check"
            />
          </v-col>
        </v-row>
        <v-btn @click="save">Fertig</v-btn>
      </v-card>
    </v-form>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import axios from 'axios';

export default {
  props: ['title', 'input'],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      maxNumber: 0,
      numberAlreadyThere: 0,
      methodOfTravels: [{
        numberOfPersons: 0,
        registration: 0,
        travelType: 1, // Reisebus
        travelTag: -1,
      }, {
        numberOfPersons: 0,
        registration: 0,
        travelType: 2, // PKW
        travelTag: -1,
      }, {
        numberOfPersons: 0,
        registration: 0,
        travelType: 3, // OEPNV
        travelTag: -1,
      }, {
        numberOfPersons: 0,
        registration: 0,
        travelType: 4, // zu fuss
        travelTag: -1,
      }, {
        numberOfPersons: 0,
        registration: 0,
        travelType: 5, // Wasserweg
        travelTag: -1,
      }],
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
  },
  created() {
    this.getMaxNumber();
    console.log(this.input);
    if (!this.input === []) {
      this.data.methodOfTravels = this.input;
    }
  },
  methods: {
    reached() {
      let sum = 0;
      this.data.methodOfTravels.forEach((i) => {
        sum += i.numberOfPersons * 1;
      });
      sum += this.data.numberAlreadyThere;
      return sum;
    },
    getMaxNumber() {
      const path = `${process.env.VUE_APP_API}basic/registration/`;
      axios
        .get(`${path}${this.$route.params.id}/participants/?&timestamp=${new Date().getTime()}`)
        .then((res) => {
          this.data.maxNumber = res.data[0].participantpersonalSet.length;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    save() {
      console.log(this.data.methodOfTravels);
      this.$emit('save', this.data.methodOfTravels);
    },
  },
};
</script>
