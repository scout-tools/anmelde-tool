<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container fluid>
      <v-row align="center" v-for="(tent, index) in this.data.tents" :key="index">
        <v-col cols="6">
          <v-subheader>
            Zelttyp
          </v-subheader>
        </v-col>
        <v-col cols="6">
          <v-select
            v-model="tent.selectedType"
            :items="data.type"
            item-text="state"
            item-value="abbr"
            label="Select"
            persistent-hint
            return-object
            single-line
          ></v-select>
        </v-col>
        <v-col cols="12">
          <v-combobox
            v-model="tent.selectedGroup"
            :items="data.groups"
            label="Gruppe"
            multiple
            outlined
            dense
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
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';
import { required, minLength, minValue } from 'vuelidate/lib/validators';

export default {
  name: 'StepNameDescription',
  props: [],
  components: {},
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
      this.validate();
      if (!this.valid) {
        return;
      }

      this.addParticipants();
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
