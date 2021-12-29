<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p>
            Bitte gebe an mit wievielen Zelten ihr kommen wollt.
            <br />
          </p>
        </span>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-col cols="2" sm="2">
          <v-text-field v-model="data.kohten" :label="`Anzahl Kohten`">
          </v-text-field>
        </v-col>
        <v-col cols="2" sm="2">
          <v-text-field
            v-if="data.kohten"
            v-model="data.kohtenstangen"
            :label="`Anzahl Kohtenstangen`"
          >
          </v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2" sm="2">
          <v-text-field v-model="data.jurten" :label="`Anzahl Jurten`">
          </v-text-field>
        </v-col>
        <v-col cols="2" sm="2">
          <v-text-field
            v-if="data.jurten"
            v-model="data.jurtenstangen"
            :label="`Anzahl Jurtenstangen`"
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

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep(true)"
        @prevStep="prevStep"
      />
    </v-container>
    <v-container v-else>
      <div class="text-center ma-5">
        <p>Lade Daten ...</p>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
        <p>Bitte hab etwas Geduld.</p>
      </div>
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';

import { required } from 'vuelidate/lib/validators';
import { stepMixin } from '@/mixins/stepMixin'; // eslint-disable-line
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepTents',
  mixins: [stepMixin],
  displayName: 'Zelte',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'scoutOrganisation',
  ],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    data: {
      kohten: 0,
      jurten: 0,
      kohtenstangen: 0,
      jurtenstangen: 0,
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'hierarchyMapping',
      'getJwtData',
      'myStamm',
      'myBund',
      'myScoutname',
    ]),
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.isLoading = true;

      Promise.all([])
        .then((values) => {
          this.test = [values];
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
