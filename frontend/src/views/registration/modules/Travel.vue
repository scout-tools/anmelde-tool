<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="nextStep"
  >
    <template v-slot:header>
      <p>Wann und wie werdet ihr voraussichtlich an ankommen?</p>
    </template>

    <template v-slot:main>
      <v-row cols="12" class="py-2">
        <p>Wann werdet ihr voraussichtlich an ankommen?</p>

        <v-btn-toggle v-model="data.time" tile color="blue accent-3" group>
          <v-btn value="left"> 16:00 - 18:00</v-btn>

          <v-btn value="center"> 18:00 - 20:00</v-btn>
          <v-btn value="right"> 20:00 - 22:00 </v-btn>
          <v-btn value="123"> 22:00 - 0:00 </v-btn>
          <v-btn value="later"> Noch Später</v-btn>
        </v-btn-toggle>
      </v-row>
      <p>Wie werdet ihr anreisen?</p>
      <v-row>
        <v-col cols="4" sm="8">
          <v-btn-toggle
            v-model="data.vehicle"
            tile
            color="blue accent-3"
            group
            multiple
          >
            <v-btn value="tain"> Bahn </v-btn>

            <v-btn value="bus"> Reisebus </v-btn>
            <v-btn value="car"> PKW </v-btn>
            <v-btn value="else"> Sonstiges </v-btn>
          </v-btn-toggle>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('car')"
            label="Wieviele PKWs?"
          >
          </v-text-field>
        </v-col>
        <v-col cols="3">
          <v-text-field
            v-show="data.vehicle.includes('else')"
            label="Sonstiges Vekehrsmittel"
          >
          </v-text-field>
        </v-col>
      </v-row>
    </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';

import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';

export default {
  name: 'StepConsent',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'currentModule',
    'personalData',
  ],
  components: {
    GenericRegModul,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    isLoading: true,
    moduleData: [],
    data: {
      vehicle: '',
      time: '',
    },
  }),
  validations: {
    data: {},
  },
  computed: {
    ...mapGetters(['userinfo']),
    isLoadingRead: {
      // getter
      get() {
        return !!this.isloading;
      },
      set() {},
    },
    moduleId() {
      return this.currentModule.module.id;
    },
    myStamm() {
      return this.userinfo.stamm;
    },
    myBund() {
      return this.userinfo.bund;
    },
    eventName() {
      return this.currentEvent.name;
    },
    cloudLink() {
      return this.currentEvent.cloudLink;
    },
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    setDefaults() {},
    loadData() {
      this.isLoading = true;
    },
  },
};
</script>
