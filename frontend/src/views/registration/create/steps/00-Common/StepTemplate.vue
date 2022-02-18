<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p>
            Bevor deine Anmeldung verbindlich wird, musst du sie im letzten
            Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang zu
            jedem Zeitpunkt unterbrechen und später fortsetzen. Die Daten kannst du
            bis zum Anmeldeschluss jederzeit
            anpassen und ergänzen. <br />
            <br />
            Die folgenden Daten sind nur für das Planungsteam und die Administrator_innen
            sichtbar. <br />
          </p>
        </span>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="`Ich stimme den Bedingungen zu und möchte mit der Anmeldung beginnen.`"
          :error-messages="checkbox1Errors"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
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
  name: 'StepConsent',
  mixins: [stepMixin],
  displayName: 'Einverständnis',
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
      checkbox1: false,
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
    ...mapGetters(['isAuthenticated', 'hierarchyMapping', 'getJwtData', 'myStamm', 'myBund', 'myScoutname']),
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
