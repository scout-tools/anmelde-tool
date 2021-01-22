<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container fluid>
      <v-row align="center" v-for="(tent, index) in this.data.tents" :key="index">
        <v-col cols="6">
          <v-select
            v-model="tent.selectedType"
            :items="data.type"
            item-text="state"
            item-value="abbr"
            label="Zelt"
            persistent-hint
            return-object
            prepend-icon="mdi-home"
          ></v-select>
        </v-col>
        <v-col cols="6">
          <v-combobox
            v-model="tent.selectedGroup"
            :items="data.groups"
            label="Gruppe"
            multiple
            outlined
            dense
            prepend-icon="mdi-human-male-female"
          ></v-combobox>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn
            elevation="5" @click="this.addTent"
          >Nächstes Zelt
          </v-btn>
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
import axios from 'axios';
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Zelte',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      type: ['Jurte', 'Kothe'],
      groups: ['Baeren', 'Adler'],
      tents: [
        { i: 0, selectedType: '', selectedGroup: '' },
      ],
    },
    dto: { registration: 7, tentType: 1, usedByScoutGroups: [] },
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
    console.log(this.getTents());
    const savedTent = { selectedType: '', selectedGroup: '', i: 1 };
    this.getTents().forEach((i, index) => {
      savedTent.selectedType = this.convertBack(i.tentType);
      savedTent.selectedGroup = i.usedByScoutGroups;
      savedTent.i = index;
      this.tents.push(savedTent);
    });
  },
  methods: {
    addTent() {
      this.data.tents.push({ i: 0, selectedType: '', selectedGroup: '' });
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
      /*  this.validate();
      if (!this.valid) {
        return;
      } */
      this.createTent();
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    convertType(typeName) {
      if (typeName === 'Kothe') {
        return 1;
      } if (typeName === 'Jurte') {
        return 2;
      }
      return null;
    },
    convertBack(typeInt) {
      if (typeInt === 1) {
        return 'Kothe';
      } if (typeInt === 2) {
        return 'Jurte';
      }
      return null;
    },
    createTent() {
      const dto = { registration: '', tentType: 1, usedByScoutGroups: [] };
      dto.registration = this.$route.params.id;
      this.data.tents.forEach((i) => {
        dto.tentType = this.convertType(i.selectedType);
        dto.usedByScoutGroups = [1]; // TODO
        axios.post(`${this.API_URL}basic/tent/`, dto);
      });
      return null;
    },
    getTents() {
      let result = [];
      axios
        .get(`${this.API_URL}basic/tent/`)
        .then((res) => {
          result = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
      return result.filter((i) => {
        console.log(i.registration);
        return i.registration === this.$route.params.id;
      });
    },
  },
};
</script>
