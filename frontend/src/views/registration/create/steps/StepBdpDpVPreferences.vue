<template>
  <v-form ref="StepBdpDpVPreferences" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <v-row v-if="dpvAddedLocation">
            <p>
              Sehr cool. Wo wollt ihr das stadt&amp;spiel spielen?.
              Du hast ein Heim / Zeltplatz hinzugefügt.
            </p>
            <v-radio-group v-model="customChoiceOne">
              <v-radio
                label="Wir wollen bei uns im Heim bleiben und besucht werden."
                value="1"
              ></v-radio>
              <v-radio
                label="Wir wollen einen anderen Stamm besuchen
                und stellen unser Heim zur Verfügung."
                value="2"
              ></v-radio>
              <v-radio
                label="Uns ist beides recht."
                value="3">
              </v-radio>
            </v-radio-group>
          </v-row>
          <v-row v-else>
            <p>
              Wo wollt ihr das stadt&amp;spiel spielen?
            </p>
          </v-row>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container
          v-show="!dpvAddedLocation || customChoiceOne === '2' || customChoiceOne === '3'"
        >
          <v-divider class="my-4" />
          <v-radio-group v-model="customChoiceTwo">
            <v-radio
              label="Wir möchten gern in der Nähe unserer Stadt bleiben.
              (Mit der Regio kommt man gut hin) "
              value="4"
            ></v-radio>
            <v-radio
              label="Wir fahren gern weit weg.
              (Im Zweifel quer durch ganz Deutschland) "
              value="5"
            >
            </v-radio>
            <v-radio
              label="Uns ist beides recht."
              value="6">
            </v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <p
        class="text-center"
        v-if="customChoiceTwo !== '0'"
        style="border-style: solid; border-color: red"
      >
        <v-icon color="pink darken-1" large class="ma-2">
          mdi-unicorn mdi-spin
        </v-icon>
        {{ textSnackbar }}
        <v-icon color="pink darken-1" large class="ma-2">
          mdi-unicorn mdi-flip-h mdi-spin
        </v-icon>
      </p>

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpVPreferences',
  displayName: 'Wohin geht es?',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    customChoiceOne: '0',
    customChoiceTwo: '0',
    snackbar: false,
    currentRegistration: [],
    textSnackbar:
      'Wir geben uns größte Mühe alle Wünsche zu berücksichtigen, können aber nichts versprechen.',
  }),
  computed: {
    ...mapGetters(['dpvAddedLocation']),
    customChoice() {
      const one = parseInt(this.customChoiceOne, 10);
      const two = parseInt(this.customChoiceTwo, 10);

      return Math.max(one, two);
    },
  },
  watch: {
    currentRegistration() {
      if (this.currentRegistration && this.currentRegistration.length) {
        this.customChoiceOne = '0';
        this.customChoiceTwo = '0';

        const status = this.currentRegistration[0].customChoice.toString(10);
        console.log(status);
        console.log(typeof status);
        if (status === '1' || status === '2' || status === '3') {
          debugger;
          this.customChoiceOne = status;
        }
        if (status === '4' || status === '5' || status === '6') {
          debugger;
          this.customChoiceTwo = status;
        }
        if (status === '0') {
          this.customChoiceOne = status;
          this.customChoiceTwo = status;
        }
      }
    },
  },
  validations: {},
  methods: {
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
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
      this.snackbar = true;
      this.patchRegiststration().then(() => {
        this.$emit('nextStep');
      });
    },
    async patchRegiststration() {
      const registrationId = this.$route.params.id;
      return axios.patch(`${process.env.VUE_APP_API}basic/registration/${registrationId}/`, {
        customChoice: this.customChoice,
      });
    },
    beforeTabShow() {
      this.loadData();
    },
    async getRegistration() {
      const registrationId = this.$route.params.id;
      const res = await axios.get(
        `${
          this.API_URL
        }basic/registration/?id=${registrationId}&timestamp=${new Date().getTime()}`,
      );
      return res.data;
    },
    loadData() {
      this.isLoading = true;
      Promise.all([this.getRegistration()])
        .then((values) => {
          [this.currentRegistration] = values;
          this.isLoading = false;
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
  },
};
</script>

<style>
</style>
