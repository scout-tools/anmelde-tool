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
          v-model="participationFee"
          :options="options"
          label="Teilnehmer_innen Beitrag"
        />
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
        @ignore="onIngoredClicked"
      />
    </v-container>
  </v-form>
</template>

<script>
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';

export default {
  name: 'StepParticipationFee',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    options: {
      locale: 'de-DE',
      prefix: '€',
      precision: 2,
    },
    participationFee: 0.0,
  }),
  methods: {
    getData() {
      return {
        participationFee: this.participationFee,
      };
    },
  },
};
</script>
