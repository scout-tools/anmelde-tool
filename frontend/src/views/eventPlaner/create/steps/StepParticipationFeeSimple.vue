<template>
  <v-form ref="StepParticipationFee">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Gib den Teilnehmerbeitrag für die Aktion an.
        </span>
      </v-row>

      <div>
        <v-card v-for="(sleep,index) in sleepingLocations" :key="index" class="my-3">
          <v-card-title>
            Schlafplatz: {{ sleep.name }}
          </v-card-title>
          <v-card-subtitle>
            <v-text-field
              v-model="sleep.name"
              :counter="100"
              label="Name des Schlafplatzes"
              required
              @input="validate"
              @blur="validate"
            />
          </v-card-subtitle>
          <v-card-actions>
            <vuetify-money
              v-model="sleep.price"
              :options="options"
              label="Teilnehmer_innen Beitrag"/>
          </v-card-actions>
        </v-card>
      </div>
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
import { isNumber } from 'lodash';
import store from '@/store';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';

export default {
  name: 'StepParticipationFeeSimple',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos'],
  mixins: [stepMixin, apiCallsMixin],
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
    test: null,
    participationFee: 0.0,
    extendedMenu: false,
    sleepingLocations: [],

  }),
  methods: {
    updateData() {
      this.sleepingLocations.forEach((item, index) => {
        if (isNumber(index)) {
          this.updateEventSleepingLocation(this.$route.params.id, item.id, item)
            .catch((error) => {
              console.log(error);
            });
        }
      });

      store.commit('createEvent/setEventAttribute', {
        prop: 'price',
        value: this.participationFee,
      });
    },
    collectSleepingLocations() {
      this.getEventSleepingLocation(this.$route.params.id)
        .then((success) => {
          this.sleepingLocations = success.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.participationFee = this.event.price;
    this.collectSleepingLocations();
  },
};
</script>
