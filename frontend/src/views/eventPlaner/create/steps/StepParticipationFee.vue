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
        :valid="true"
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';

export default {
  name: 'StepParticipationFee',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  computed: {
    ...mapGetters({
      event: 'createEvent/event',
    }),
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
    updateData() {
      store.commit('createEvent/setEventAttribute', {
        prop: 'price',
        value: this.participationFee,
      });
    },
  },
  mounted() {
    this.participationFee = this.event.price;
  },
};
</script>
