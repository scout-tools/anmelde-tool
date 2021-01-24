<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container fluid>
      <v-row align="center" v-for="(tent, index) in this.data.tents" :key="index">
        <v-col cols="5">
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
        <v-col cols="5">
          <v-select
            v-model="tent.selectedGroups"
            :items="scoutGroupMapping"
            item-text="name"
            item-value="id"
            label="Gruppe"
            multiple
            outlined
            dense
            prepend-icon="mdi-human-male-female"
          ></v-select>
        </v-col>
        <v-col cols="2">
          <v-btn icon @click="deleteTent(index)">
            <v-icon>mdi-trash-can</v-icon>
          </v-btn>
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
    deleteTent(id) {
      console.log(id);
      axios
        .delete(`${this.API_URL}basic/tent/${this.data.tents[id].i}/`)
        .catch((err) => {
          console.log(err);
        });
      this.data.tents.splice(id, 1);
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
        console.log(i);
        if (i.i.isEmpty || i.i === 0) {
          dto.tentType = i.selectedType;
          i.selectedGroups.forEach((group) => dto.usedByScoutGroups.push(group));
          axios.post(`${this.API_URL}basic/tent/`, dto);
          dto.usedByScoutGroups = [];
        } else {
          dto.tentType = i.selectedType;
          i.selectedGroups.forEach((group) => dto.usedByScoutGroups.push(group));
          axios.put(`${this.API_URL}basic/tent/${i.i}/`, dto);
          dto.usedByScoutGroups = [];
        }
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
      this.registeredTents.forEach((i) => {
        const savedTent = { selectedType: '', selectedGroups: [], i: 1 };
        if (parseInt(i.registration, 10) === parseInt(this.$route.params.id, 10)) {
          this.tentTypeMapping.forEach((type) => {
            if (i.tentType === type.id) {
              savedTent.selectedType = type.id;
            }
          });
          savedTent.selectedGroups = i.usedByScoutGroups;
          savedTent.i = i.id;
          this.data.tents.push(savedTent);
        }
      });
      if (this.data.tents.length > 1) {
        this.data.tents.splice(0, 1);
      }
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
