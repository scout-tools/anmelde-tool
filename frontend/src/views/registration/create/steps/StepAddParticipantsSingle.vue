<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
    <v-btn
      color="success"
      @click="newUser"
    >
      <v-icon left>
        mdi-plus
      </v-icon>
      Neuen Teilnehmer hinzufügen
    </v-btn>
    <v-list>
      <v-subheader>Teilnehmer</v-subheader>
      <v-list-item-group
        color="primary"
      >
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
        >
        <v-list-item-avatar>
          <v-icon
          color="black"
            dark
            v-text="item.icon"
          ></v-icon>
        </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item-content>
        <v-list-item-action>
          <v-btn dense icon>
            <v-icon color="grey lighten-1">mdi-information</v-icon>
          </v-btn>
        </v-list-item-action>
        </v-list-item>

      </v-list-item-group>
    </v-list>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-single-person-dialog ref="createSinglePersonDialog"/>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import CreateSinglePersonDialog from './dialog/CreateSinglePersonDialog.vue';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
    CreateSinglePersonDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    selectedItem: 1,
    items: [
      { text: 'Thea', icon: 'mdi-account' },
      { text: 'Robert', icon: 'mdi-account' },
      { text: 'Alina', icon: 'mdi-account' },
    ],
  }),
  validations: {},
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchyMapping', 'ageGroupMapping']),
    total() {
      return Object.values(this.data).reduce((pv, cv) => parseInt(pv, 10) + parseInt(cv, 10), 0);
    },
    getActiveAgeGroups() {
      if (
        this.ageGroupMapping
        && this.currentEvent
        && this.currentEvent.ageGroups
        && this.currentEvent.ageGroups.length
      ) {
        return this.ageGroupMapping.filter((item) => this.currentEvent.ageGroups.includes(item.id));
      }
      return [];
    },
  },
  methods: {
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

      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    addParticipants() {
      const promises = [];
      const registrationId = this.$route.params.id;
      const myUrl = `${this.API_URL}basic/participant/`;
      const valueArray = Object.values(this.data);
      Object.keys(this.data).forEach((element, index) => {
        const paramsData = {
          ageGroup: parseInt(element, 10),
          numberOfPersons: parseInt(valueArray[index], 10),
          registration: parseInt(registrationId, 10),
        };
        promises.push(axios.post(myUrl, paramsData));
      });

      Promise.all(promises).then(() => {
        this.$emit('nextStep');
      });
    },
    newUser() {
      this.$refs.createSinglePersonDialog.openDialog();
    },
  },
};
</script>