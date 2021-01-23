<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container fluid>
      <v-row align="center" v-for="(tent, index) in this.data.tents" :key="index">
        <v-col cols="6">
          <v-select
            v-model="tent.selectedType"
            :items="tentTypeMapping"
            item-text="name"
            item-value="id"
            label="Zelt"
            persistent-hint
            prepend-icon="mdi-home"
          ></v-select>
        </v-col>
        <v-col cols="6">
          <v-combobox
            v-model="tent.selectedGroups"
            :items="scoutGroupMapping"
            item-text="name"
            item-value="id"
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
      groups: [
        { id: 1, name: '' },
      ],
      tents: [
        { i: 0, selectedType: '', selectedGroups: [] },
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
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping', 'ageGroupMapping', 'tentTypeMapping', 'scoutGroupMapping', 'registeredTents']),
    total() {
      return Object.values(this.data).reduce((pv, cv) => parseInt(pv, 10) + parseInt(cv, 10), 0);
    },
  },
  created() {
    this.getGroups();
    this.getTentTypes();
    this.getTents();
    this.convertSavedTents();
  },
  methods: {
    addTent() {
      this.data.tents.push({ i: 0, selectedType: '', selectedGroups: [] });
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
    createTent() {
      const dto = { registration: '', tentType: 1, usedByScoutGroups: [] };
      dto.registration = this.$route.params.id;
      this.data.tents.forEach((i) => {
        dto.tentType = i.selectedType;
        i.selectedGroups.forEach((group) => dto.usedByScoutGroups.push(group.id));
        axios.post(`${this.API_URL}basic/tent/`, dto);
      });
      return null;
    },
    getTents() {
      axios
        .get(`${this.API_URL}basic/tent/?&timestamp=${new Date().getTime()}`)
        .then((res) => this.$store.commit('setRegisteredTents', res.data))
        .catch((err) => {
          console.log(err);
        });
    },
    getTentTypes() {
      axios
        .get(`${this.API_URL}basic/tent-type/`)
        .then((res) => this.$store.commit('setTentTypeMapping', res.data))
        .catch((err) => {
          console.log(err);
        });
    },
    convertSavedTents() {
      const savedTent = { selectedType: '', selectedGroups: [], i: 1 };
      this.registeredTents.forEach((i, index) => {
        if (parseInt(i.registration, 10) === parseInt(this.$route.params.id, 10)) {
          console.log(`Type: ${i.tentType}ScoutGroups: ${i.usedByScoutGroups}`);
          savedTent.selectedType = this.tentTypeMapping
            .filter((type) => i.tentType === type.id)[0].name;
          savedTent.selectedGroups = i.usedByScoutGroups;
          savedTent.i = index;
          this.data.tents.push(savedTent);
        } else {
          console.log('nothing');
        }
      });
    },
    getGroups() {
      axios
        .get(`${this.API_URL}basic/scout-hierarchy-group/?&timestamp=${new Date().getTime()}`)
        .then((res) => {
          this.$store.commit('setScoutGroupMapping', res.data);
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
