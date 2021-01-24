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
              v-model="data.numberBus"
              label="Bus"
              required
              @input="$v.data.numberBus.$touch()"
              @blur="$v.data.numberBus.$touch()"
              prepend-icon="mdi-bus"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.numberCar"
              label="PKW"
              required
              @input="$v.data.numberCar.$touch()"
              @blur="$v.data.numberCar.$touch()"
              prepend-icon="mdi-car"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.numberPublic"
              label="OEPNV"
              required
              @input="$v.data.numberPublic.$touch()"
              @blur="$v.data.numberPublic.$touch()"
              prepend-icon="mdi-bus-stop"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.numberWalking"
              label="zu Fuss"
              required
              @input="$v.data.numberWalking.$touch()"
              @blur="$v.data.numberWalking.$touch()"
              prepend-icon="mdi-hiking"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.numberWater"
              label="Wasserweg"
              required
              @input="$v.data.numberWater.$touch()"
              @blur="$v.data.numberWater.$touch()"
              prepend-icon="mdi-ship-wheel"
            />
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="data.numberAlreadyThere"
              label="Schon da"
              required
              @input="$v.data.numberAlreadyThere.$touch()"
              @blur="$v.data.numberAlreadyThere.$touch()"
              prepend-icon="mdi-account-check"
            />
          </v-col>
        </v-row>
      </v-card>
    </v-form>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import axios from 'axios';

export default {
  props: ['title'],
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
      numberAlreadyThere: 0,
      infos: ['Anreise', 'Abreise'],
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
  },
  methods: {
    reached() {
      // eslint-disable-next-line max-len
      const sum = this.data.numberBus * 1 + this.data.numberCar * 1 + this.data.numberPublic * 1 + this.data.numberWalking * 1 + this.data.numberWater * 1;
      return sum;
    },
    getMaxNumber() {
      axios
        .get(`${this.API_URL}basic/registration/${this.$route.params.id}/participants/?&timestamp=${new Date().getTime()}`)
        .then((res) => {
          this.data.maxNumber = res.data[0].participants.length;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
