<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="mt-2">
        <span class="ma-5 subtitle-1">
          <p>
            Bitte teilt uns mit, welche Zelte ihr in Mosaikersleben
            aufschlagen möchtet und ordnet alle Gruppen den Zelten zu,
            wir reservieren euch dann schon mal die besten Liegeplätze.
          </p>
  <v-expansion-panels flat>
    <v-expansion-panel>
      <v-expansion-panel-header>
        Habt ihr andere Zelte? (klicke hier zum aufklappen)
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        Wenn ihr andere Zelte als Kohten oder Jurten nutzt, dann wählt
        einfach das aus was der Grundfläche eures Zeltes am nächsten kommt.
        Wenn ihr zum Beispiel in einem Kamel schlaft, dann ordnet ihr einer
        Gruppe zwei Kohten zu. Es ist möglich ein Zelt mehreren Gruppen zuzuordnen
        oder eine Gruppe auf mehrere Zelte aufzuteilen (z.B. die freien Rover).
        Wählt dazu die Gruppe einfach bei mehreren Zelten aus oder umgekehrt, die
        genaue Aufteilung ist für uns nicht wichtig und wird daher nicht erfragt.
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
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
            dense
            persistent-hint
            prepend-icon="mdi-home"
            :error-messages="selectedTypeError(index)"
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
            chips
            dense
            prepend-icon="mdi-human-male-female"
            :error-messages="selectedGroupsError(index)"
          ></v-select>
        </v-col>
        <v-col cols="2">
          <v-btn fab icon @click="deleteTent(index)">
            <v-icon color="red">mdi-trash-can</v-icon>
          </v-btn>
        </v-col>
      </v-row>
      <v-divider/>
      <v-row>
        <v-col>
          <v-btn color="success" @click="this.addTent">
            <v-icon>mdi-plus</v-icon>
            Weiteres Zelt
          </v-btn>
        </v-col>
      </v-row>
      <v-row v-if="data.errorTent" style="color:red">
        Lege mindestens ein Zelt an.
      </v-row>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
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
import { required, minLength } from 'vuelidate/lib/validators';
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

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
      tents: [
        { i: 0, selectedType: null, selectedGroups: null },
      ],
      errorTent: false,
    },
  }),
  validations: {
    data: {
      tents: {
        required,
        minLength: minLength(2),
        $each: {
          selectedType: {
            required,
          },
          selectedGroups: {
            required,
            $each: {
              required,
            },
          },
        },
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
    selectedTypeError(index) {
      const errors = [];
      if (!this.$v.data.tents.$each[index].selectedType.required) {
        errors.push('Zelt ist erforderlich');
      }
      return errors;
    },
    selectedGroupsError(index) {
      const errors = [];

      if (!this.$v.data.tents.$each[index].selectedGroups.required) {
        errors.push('Gruppe ist erforderlich');
      }
      return errors;
    },
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
      this.data.tents.push({ i: 0, selectedType: null, selectedGroups: null });
      this.getGroups()
        .then((res) => this.$store.commit('setScoutGroupMapping', res))
        .catch((error) => {
          console.log(error);
        });
      this.data.errorTent = false;
    },
    deleteTent(id) {
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
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();

      if (!this.valid) {
        return;
      }
      this.createTent();
      this.$emit('nextStep');
    },
    createTent() {
      const dto = {
        registration: this.$route.params.id,
        tentType: 1,
        usedByScoutGroups: [],
      };
      this.data.tents.forEach((i) => {
        if (i.i.isEmpty || i.i === 0) {
          dto.tentType = i.selectedType;
          i.selectedGroups.forEach((group) => dto.usedByScoutGroups.push(group));
          axios.post(`${this.API_URL}basic/tent/`, dto);
        } else {
          dto.tentType = i.selectedType;
          i.selectedGroups.forEach((group) => dto.usedByScoutGroups.push(group));
          axios.put(`${this.API_URL}basic/tent/${i.i}/`, dto);
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
        const savedTent = { selectedType: null, selectedGroups: null, i: -1 };
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
