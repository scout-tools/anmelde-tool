<template>
  <v-form ref="StepParticipationFee">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Gib den Teilnehmerbeitrag für die Aktion an. Dafür gibt es mehrere Optionen, entweder gibt
          es eine Schlafkategorie mit einem fixen Betrag,
          dann einfach unten den Betrag eintragen und
          weiter gehts. Brauchst du allerdings mehr Optionen,
          weil es z.B. verschiedene Übernachtungsmöglichkeiten gibt
          oder es einen Frühbucher Rabatt geben soll, dann geht es ab ins erweiterte Menü.
        </span>
      </v-row>
      <v-switch label="Erweitere Menü" v-model="extendedMenu"></v-switch>
      <!--      <div v-if="!extendedMenu">-->
      <!--        <v-row>-->
      <!--          <vuetify-money-->
      <!--            v-model="participationFee"-->
      <!--            :options="options"-->
      <!--            label="Teilnehmer_innen Beitrag"-->
      <!--          />-->
      <!--        </v-row>-->
      <!--      </div>-->
      <div>
        <v-card v-for="(sleep,index) in sleepingLocations" :key="index" class="my-3">
          <v-card-title>
            <v-btn v-if="sleepingLocations.length > 1" icon color="red"
                   @click="deleteSleepingLocation(sleep.id)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
            Schlafplatz: {{ sleep.name }}
          </v-card-title>
          <v-card-subtitle>
            <v-text-field
              v-model="sleep.name"
              :counter="100"
              label="Beschreibung des Schlafplatzes"
              required
              @input="validate"
              @blur="validate"
            />
          </v-card-subtitle>
          <v-card-subtitle>
            <v-text-field
              v-model="sleep.description"
              :counter="100"
              label="Beschreibung des Schlafplatzes"
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

          <v-card-text>
            Du kannst auch angeben ob ein Schlafplatz zeitlich begrenzt buchbar ist.
            Damit kannst du z.B. Frühbucher Rabatte einstellen
            und diese im Vergleich zu unbegrenzt buchbaren Schlafplätzen vergünstigen.
          </v-card-text>
          <v-card-actions>
            <DateTimePicker
              :ref="'bookableTillRef-' + sleep.id"
              v-model="sleep.bookableTill"
              title="Buchbar bis"
            />
          </v-card-actions>

        </v-card>

        <v-row class="align-center justify-center text-center">
          <v-btn depressed @click="addSleepingLocation" class="my-3"
                 color="secondary" elevation="2">
            Weitere Schlafmöglichkeit
          </v-btn>
        </v-row>
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
import moment from 'moment';
import { isNumber } from 'lodash';
import Vue from 'vue';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import DateTimePicker from '@/components/picker/DateTimePicker.vue';

export default {
  name: 'StepParticipationFee',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos'],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    PrevNextButton,
    DateTimePicker,
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
    setTimes() {
      this.sleepingLocations.forEach((item, index) => {
        if (isNumber(index)) {
          const time = moment(item.bookableTill)
            .toDate();
          this.sleepingLocations[index].bookableTill = time;
          const ref = `bookableTillRef-${item.id}`;
          if (this.$refs[ref]) {
            console.log('found ref');
            this.$refs[ref][0].setDate(time);
          }
        }
      });
    },
    addSleepingLocation() {
      this.addEventSleepingLocation(this.$route.params.id)
        .then(() => {
          this.collectSleepingLocations();
        });
    },
    collectSleepingLocations() {
      this.getEventSleepingLocation(this.$route.params.id)
        .then((success) => {
          this.sleepingLocations = success.data;
          this.extendedMenu = this.sleepingLocations.length > 1;
          Vue.nextTick()
            .then(() => {
              this.setTimes();
            });
        })
        .catch((error) => {
          console.log(error);
        });
    },
    deleteSleepingLocation(id) {
      this.deleteEventSleepingLocation(this.$route.params.id, id)
        .then(() => {
          this.collectSleepingLocations();
        });
    },

  },
  mounted() {
    this.participationFee = this.event.price;
    this.collectSleepingLocations();
  },
  watch: {
    extendedMenu(newVal) {
      if (newVal) {
        Vue.nextTick()
          .then(() => {
            this.setTimes();
          });
      }
    },
  },
};
</script>
