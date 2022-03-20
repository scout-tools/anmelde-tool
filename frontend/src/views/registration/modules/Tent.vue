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
          <p>
            Bitte gebe an mit wievielen Zelten ihr kommen wollt.
            <br />
          </p>
    </template>

    <template v-slot:main>
      <v-row>
        <v-col cols="5">
          <v-text-field v-model="data.kohten" :label="`Anzahl Kohten`">
          </v-text-field>
        </v-col>
        <v-col cols="5">
          <v-text-field
            v-if="data.kohten"
            v-model="data.kohtenstangen"
            :label="`Anzahl benötigter Kohtenstangen`"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="5">
          <v-text-field v-model="data.jurten" :label="`Anzahl Jurten`">
          </v-text-field>
        </v-col>
        <v-col cols="5">
          <v-text-field
            v-if="data.jurten"
            v-model="data.jurtenstangen"
            :label="`Anzahl benötigter Jurtenstangen`"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row align="center" justify="center">
        <p
          class="text-center"
          v-if="data.jurtenstangen || data.kohtenstangen"
          style="border-style: solid; border-color: red"
        >
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-spin
          </v-icon>
          Zeltstangen sind nur begrenzt verfügbar. Bitte nutzt Steckstangen,
          wenn ihr welche zur Verfügung habt.
          <v-icon color="red darken-1" large class="ma-2">
            mdi-alert mdi-flip-h mdi-spin
          </v-icon>
        </p>
        <p
          class="text-center"
          v-if="
            !data.jurtenstangen &&
            !data.kohtenstangen &&
            (data.jurten > 0 || data.kohten > 0)
          "
          style="border-style: solid; border-color: green"
        >
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline
          </v-icon>
          Mega Cool, dass ihr eure Zeltstangen selbst mitbringt.
          <v-icon color="green darken-1" large class="ma-2">
            mdi-emoticon-kiss-outline mdi-flip-h
          </v-icon>
        </p>
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
    },
  }),
  validations: {
    data: {
    },
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
    setDefaults() {
    },
    loadData() {
      this.isLoading = true;
    },
  },
};
</script>
