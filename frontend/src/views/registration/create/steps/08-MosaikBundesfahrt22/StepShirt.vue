<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row>
        <span class="subtitle-1">
          <p>Wieviele T-Shirts wollt ihr bestellen?</p>
        </span>
      </v-row>
      <v-row
        align="center"
        v-for="(shirt, index) in this.shirtSizes"
        :key="index"
      >
        <v-col cols="5">
          <span> {{ shirt.name}} </span>
        </v-col>
        <v-col cols="5">
          <v-text-field label="Stück">

          </v-text-field>
        </v-col>
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
// import axios from 'axios';
import { stepMixin } from '@/mixins/stepMixin';
import { mapGetters } from 'vuex';
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepShirt',
  displayName: 'T-Shirts',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: false,
    data: {
      tents: [{ i: 0, selectedType: null, selectedGroups: null }],
    },
    shirtSizes: [
      {
        id: 1,
        name: 'XS',
      },
      {
        id: 2,
        name: 'S',
      },
      {
        id: 3,
        name: 'M',
      },
      {
        id: 4,
        name: 'L',
      },
      {
        id: 5,
        name: 'XL',
      },
      {
        id: 6,
        name: 'XXL',
      },
    ],
  }),
  validations: {
    data: {
    },
  },
  computed: {
    ...mapGetters([
    ]),
  },
  methods: {
    getData() {
    },
    beforeTabShow() {
      this.data.tents = [];
      this.getData();
    },
  },
};
</script>
