<template>
  <v-form ref="StepParticipationFee">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Gib den Teilnehmerbeitrag für die Aktion an.
        </span>
      </v-row>
      <v-row>
        <vuetify-money
          v-model="data.participationFee"
          :options="options"
          label="Teilnehmer_innen Beitrag"
        />
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep()"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepParticipationFee',
  props: ['position', 'maxPos', 'data'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    options: {
      locale: 'de-DE',
      prefix: '€',
      precision: 2,
    },
  }),
  methods: {
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.$emit('nextStep');
    },
    submitStep() {
      this.$emit('submit');
    },
    getData() {
      return {
        participationFee: this.data.participationFee,
      };
    },
  },
};
</script>
