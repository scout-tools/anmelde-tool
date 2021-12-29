<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container v-if="!isLoading">
      <v-row class="ma-3">
        <h4 v-if="!data.registrationType" class="text-left">
          Wähle die Art deiner Anmeldung
        </h4>
      </v-row>
      <!-- <v-row>
        <v-btn
          @click="setRegistrationType('organisation')"
          x-large
          class="ma-3"
          :color="getColor('organisation')"
        >
          <v-icon left> mdi-account-group </v-icon>
          Stammesanmeldung
        </v-btn>
        <v-btn
          @click="setRegistrationType('single')"
          x-large
          class="ma-3"
          :color="getColor('single')"
        >
          <v-icon left> mdi-account-plus </v-icon>
          Einzelanmeldung
        </v-btn>
      </v-row> -->
      <v-row>
        <v-radio-group v-model="data.registrationType">
          <v-radio
            v-for="registrationTyp in registrationTypes"
            :key="registrationTyp.id"
            :label="registrationTyp.name"
            :value="registrationTyp.techname"
          ></v-radio>
        </v-radio-group>
      </v-row>
      <transition-group name="fade">
        <v-row
          key="1"
          class="mt-2"
          v-if="
            data.registrationType && data.registrationType === 'group'
          "
        >
          <span class="text-left subtitle-1">
            <p>
              Hiermit melde ich den Stamm <b> {{ myStamm }} </b> aus dem Bund
              <b> {{ myBund }} </b> zu <b> {{ currentEvent.name }} </b> an.
              <br />
              <br />
              Bevor deine Anmeldung verbindlich wird, musst du sie im letzten
              Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang
              zu jedem Zeitpunkt unterbrechen und später fortsetzen. Die Daten
              kannst du bis zum Anmeldeschluss ({{
                registrationDeadlineFormat
              }}) jederzeit anpassen und ergänzen. <br />
              <br />
              Die folgenden Daten sind nur für das Planungsteam und die
              Administrator_innen sichtbar. <br />
              <span v-if="isBundesfahrt">Alle Dokumente findest du hier:</span>
              <a
                v-if="isBundesfahrt"
                target="_blank"
                href="https://cloud.dpvonline.de/s/5BM6qmNS5Mp7wqG"
                style="color:blue;"
              >
                Link zur DPV-Cloud
              </a>
            </p>
          </span>
        </v-row>
        <v-row
          key="33"
          class="mt-2"
          v-if="data.registrationType && data.registrationType === 'single'"
        >
          <span class="text-left subtitle-1">
            <p>
              Hiermit melde ich mich vom<b> {{ myStamm }} </b> aus dem Bund
              <b> {{ myBund }} </b> zu <b> {{ currentEvent.name }} </b> an.
              <br />
              <br />
              Bevor deine Anmeldung verbindlich wird, musst du sie im letzten
              Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang
              zu jedem Zeitpunkt unterbrechen und später fortsetzen. Die Daten
              kannst du bis zum Anmeldeschluss ({{
                registrationDeadlineFormat
              }}) jederzeit anpassen und ergänzen. <br />
              <br />
              Die folgenden Daten sind nur für das Planungsteam und die
              Administrator_innen sichtbar. <br />
              <span v-if="isBundesfahrt">Alle Dokumente findest du hier:</span>
              <a
                v-if="isBundesfahrt"
                target="_blank"
                href="https://cloud.dpvonline.de/s/5BM6qmNS5Mp7wqG"
                style="color:blue;"
              >
                Link zur DPV-Cloud
              </a>
            </p>
          </span>
        </v-row>
        <v-divider
          key="65"
          class="text-left my-2"
          v-if="data.registrationType"
        />
        <v-row
          key="2"
          v-if="
            data.registrationType && data.registrationType === 'group'
          "
        >
          <v-checkbox
            v-model="data.checkbox1"
            :label="
              `Ich bin von meinem Stamm bevollmächtigt und stimme für` +
              `meinen Stamm die Bedingungen zu und möchte mit der Stammes-Anmeldung beginnen.`
            "
            :error-messages="errorMessage('checkbox1')"
          >
          </v-checkbox>
        </v-row>

        <v-row
          key="22"
          v-if="data.registrationType && data.registrationType === 'single'"
        >
          <v-checkbox
            v-model="data.checkbox1"
            :label="`Ich stimme den Bedingungen zu und möchte mit der Einzel-Anmeldung beginnen.`"
            :error-messages="errorMessage('checkbox1')"
          >
          </v-checkbox>
        </v-row>

        <v-row v-if="data.registrationType" key="3">
          <v-checkbox
            v-model="data.checkbox2"
            v-if="isBundesfahrt"
            :label="`Hiermit bestätige ich, dass alle Teilnehmer_innen,
          die ich auf diesem Wege zu ${currentEvent.name} anmelde die
          Datenschutzhinweise zur
          Kenntnis genommen und diesen zugestimmt haben.`"
            :error-messages="errorMessage('checkbox2')"
          >
          </v-checkbox>
        </v-row>

        <v-row v-if="data.registrationType" key="4">
          <v-checkbox
            v-model="data.checkbox3"
            v-if="isBundesfahrt"
            :label="`Ich trage Sorge, dass alle von mir angemeldeten Teilnehmer_innen
            über die Coronaregel informiert sind
            und ich achte auf die Einhaltung.`"
            :error-messages="errorMessage('checkbox3')"
          >
          </v-checkbox>
        </v-row>

        <v-divider class="my-3" key="66" />

        <prev-next-buttons
          key="5"
          v-if="data.registrationType"
          :position="position"
          :max-pos="maxPos"
          @nextStep="nextStep"
          @prevStep="prevStep"
        />
      </transition-group>
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
import moment from 'moment';
import axios from 'axios';

import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepConsent',
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
    registrationTypes: [
      { id: 1, name: 'Gruppenanmeldung', techname: 'group' },
      { id: 2, name: 'Einzelanmeldung', techname: 'single' },
    ],
    data: {
      checkbox1: false,
      checkbox2: false,
      checkbox3: false,
      registrationType: false,
      name: '',
      description: '',
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
      checkbox2: {
        function(value) {
          return value === true || !this.isBundesfahrt;
        },
      },
      checkbox3: {
        function(value) {
          return value === true || !this.isBundesfahrt;
        },
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
    registrationDeadlineFormat() {
      return moment(this.currentEvent.registrationDeadline)
        .lang('de')
        .format('ll');
    },
    myEmail() {
      return this.getJwtData.email;
    },
    isBundesfahrt() {
      if (this.currentEvent) {
        return this.currentEvent.eventTags.filter((tag) => tag === 1).length;
      }
      return false;
    },
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    getRegistrationTypeString() {
      if (this.data.registrationType === 'single') {
        return 'Einzelanmeldung';
      }
      if (this.data.registrationType === 'group') {
        return 'Gruppenanmelung';
      }
      return 'Fehler';
    },
    getColor(registrationType) {
      if (!this.data.registrationType) {
        return 'primary';
      }
      return this.data.registrationType === registrationType
        ? 'success'
        : 'lightgrey';
    },
    errorMessage(field) {
      const errors = [];
      const valObj = this.$v.data[field];
      if (!valObj.$dirty) return errors;
      if (valObj.required === false) {
        errors.push('Dieses Feld ist erforderlich.');
      }
      if (valObj.minLength === false) {
        const { min } = valObj.$params.minLength;
        errors.push(`Du musst mindestens ${min} Zeichen nutzen.`);
      }
      if (valObj.maxLength === false) {
        const { max } = valObj.$params.maxLength;
        errors.push(`Du darfst maximal ${max} Zeichen nutzen.`);
      }
      if (valObj.minValue === false) {
        errors.push(`Minimal sind ${valObj.$params.minValue.min} erlaubt.`);
      }
      if (valObj.maxValue === false) {
        errors.push(`Maximal sind ${valObj.$params.maxValue.max} erlaubt.`);
      }
      if (valObj.between === false) {
        const { min, max } = valObj.$params.between;
        errors.push(
          `Bitte gib einen Wert zwischen ${min}€ und ${max}€ ein. Falls du mehr als ${max} brauchst melde dich bei der Lagerleitung.`,
        );
      }
      return errors;
    },
    setRegistrationType(value) {
      this.data.registrationType = value;
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
      this.$emit('nextStep');
    },
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.isLoading = true;

      Promise.all([this.loadUserExtended()])
        .then((values) => {
          this.setMyStamm(values[0]);
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    setMyStamm(data) {
      let myStamm = 'kein Stamm';
      if (data.scoutOrganisation) {
        myStamm = this.hierarchyMapping.find(
          (item) => item.id === data.scoutOrganisation,
        ).name;
        const parentId = this.hierarchyMapping.find(
          (item) => item.id === data.scoutOrganisation,
        ).parent;
        let parentObj = this.hierarchyMapping.find(
          (item) => item.id === parentId,
        );
        if (parentObj.level > 3) {
          parentObj = this.hierarchyMapping.find(
            (item) => item.id === parentObj.parent,
          );
        }
        this.$store.commit('setMyBund', parentObj.name);
        this.$store.commit('setMyStamm', myStamm);
        this.$store.commit('setMyScoutname', data.scoutName);
      }
    },
    async loadUserExtended() {
      const path = `${this.API_URL}/auth/data/user-extended/${this.getJwtData.userId}/`;
      const response = await axios.get(path);

      return response.data;
    },
  },
};
</script>

<style scoped>
.fade-enter-active {
  transition: opacity 2s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
