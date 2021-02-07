<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="mt-2">
        <span class="text-center ma-5 subtitle-1">
          <p>
            Bitte gebt die Zelte an, die ihr in Mosaikersleben nutzen wollt
            und ordnet alle Gruppen den Zelten zu. Wenn ihr andere Zelte als
            Kohte oder Jurte nutzt, ordnet bitte eure Grundfläche einem der beiden Zelte zu.
          </p>
        </span>
      </v-row>
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
            <v-icon color="red">mdi-trash-can</v-icon>
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
    <v-container v-else>
      <div class="text-center ma-5">
        <v-progress-circular
          :size="80"
          :width="10"
          color="primary"
          indeterminate
        ></v-progress-circular>
      </div>
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepTents',
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
  methods: {
    getData() {
      this.isLoading = true;
      Promise.all([
        this.getGroups(),
        this.getTentTypes(),
        this.getTents(),
      ])
        .then((values) => {
          this.$store.commit('setScoutGroupMapping', values[0]);
          this.$store.commit('setTentTypeMapping', values[1]);
          this.$store.commit('setRegisteredTents', values[2].filter((i) => parseInt(i.registration, 10) === parseInt(this.$route.params.id, 10)));
          this.convertSavedTents();
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
    addTent() {
      this.data.tents.push({ i: 0, selectedType: '', selectedGroups: [] });
      this.getGroups()
        .then((res) => this.$store.commit('setScoutGroupMapping', res))
        .catch((error) => {
          console.log(error);
        });
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
    async getTents() {
      const res = await axios
        .get(`${this.API_URL}basic/tent/?&timestamp=${new Date().getTime()}`);
      return res.data;
    },
    async getTentTypes() {
      const res = await axios
        .get(`${this.API_URL}basic/tent-type/`);
      return res.data;
    },
    convertSavedTents() {
      this.registeredTents.forEach((i) => {
        const savedTent = { selectedType: '', selectedGroups: [], i: -1 };
        this.tentTypeMapping.forEach((type) => {
          if (i.tentType === type.id) {
            savedTent.selectedType = type.id;
          }
        });
        savedTent.selectedGroups = i.usedByScoutGroups;
        savedTent.i = i.id;
        this.data.tents.push(savedTent);
      });
      // if (this.data.tents.length > 1) {
      //   this.data.tents.splice(0, 1);
      // }
    },
    async getGroups() {
      const res = await axios
        .get(`${this.API_URL}basic/scout-hierarchy-group/?&timestamp=${new Date().getTime()}`);
      return res.data;
    },
    beforeTabShow() {
      this.data.tents = [];
      this.getData();
    },
  },
};
</script>
