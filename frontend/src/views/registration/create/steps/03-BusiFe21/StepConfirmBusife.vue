<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row class="mt-2">
         <!-- <div class="text-left subtitle-1">
          <p><b>Zusammenfassung</b></p>
            Ihr habt {{ participantCount }} Teilnehmende und {{ workshopCount }} AGs angemeldet.
        </div> -->
      </v-row>
       <v-divider class="text-left my-2"/>
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :error-messages="errorMessage"
          :label="`Ich habe meine Daten überprüft und melde meinen Stamm verbindlich zur Fahrt an.`"
          @change="validate"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

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
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import PrevNextButtons from '../../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepConfirmBundesfahrt',
  displayName: 'Zusammenfassung und Bestätigung',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    participantCount: null,
    workshopCount: null,
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
    id() {
      return this.$route.params.id;
    },
    errorMessage() {
      return (this.valid) ? '' : 'Um dich anmelden zu können, musst du hier bestätigen.';
    },
  },
  methods: {
    async loadData() {
      this.isLoading = true;
      const response = await Promise.all(
        [this.loadParticipants(), this.loadWorkshops()],
      );
      this.participantCount = response[0][0].participantpersonalSet.length;
      this.workshopCount = response[1].length;
      this.isLoading = false;
    },
    async loadParticipants() {
      const path = `${this.API_URL}basic/registration/${this.$route.params.id}/participants/?&timestamp=${new Date().getTime()}`;
      const response = await axios.get(path);

      return response.data;
    },
    async loadWorkshops() {
      const path = `${this.API_URL}basic/workshop/?registration=${this.$route.params.id}&timestamp=${new Date().getTime()}`;
      const response = await axios.get(path);

      return response.data;
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
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    onRefresh() {
      this.loadData();
      this.valid = true;
    },
    getData() {
      return {};
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
};
</script>
