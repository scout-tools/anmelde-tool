<template>
  <v-container class="mt-10">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card>
            <v-tabs
              v-model="tab"
              background-color="primary"
              grow
              centered
              dark
              icons-and-text
            >
              <v-tabs-slider></v-tabs-slider>

              <v-tab href="#tab-1">
                Anmeldungen
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab href="#tab-2">
                Karte
                <v-icon>mdi-map</v-icon>
              </v-tab>

              <v-tab href="#tab-3">
                Kasse
                <v-icon>mdi-currency-eur</v-icon>
              </v-tab>
              <v-tab href="#tab-4">
                Küche
                <v-icon>mdi-silverware-fork-knife</v-icon>
              </v-tab>
              <v-tab href="#tab-5">
                Program
                <v-icon>mdi-silverware-fork-knife</v-icon>
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="i in 5" :key="i" :value="'tab-' + i">
                <v-card-text>
                  <registration-main v-if="i === 1" />
                  <maps-main v-if="i === 2" />
                  <cash-main v-if="i === 3" />
                  <kitchen-main v-if="i === 4" />
                  <program-main v-if="i === 5" />
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

import MapsMain from '@/views/statistic/maps/Main.vue';
import RegistrationMain from '@/views/statistic/registration/Main.vue';
import CashMain from '@/views/statistic/cash/Main.vue';
import ProgramMain from '@/views/statistic/program/Main.vue';
import KitchenMain from '@/views/statistic/kitchen/Main.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    MapsMain,
    RegistrationMain,
    CashMain,
    KitchenMain,
    ProgramMain,
  },
  computed: {
    ...mapGetters(['currentEventParticipants', 'currentEventCash', 'currentEventKitchen', 'currentEventProgram']),
    eventId() {
      return this.$route.params.id;
    },
  },
  data() {
    return {
      tab: null,
      selected: null,
    };
  },
  asyncComputed: {
    async getParticipantsData() {
      const path = `${process.env.VUE_APP_API}basic/event/${this.eventId}/participants/`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setCurrentEventParticipants', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    async getCashData() {
      const path = `${process.env.VUE_APP_API}basic/event/${this.eventId}/cash-eventmaster-overview/`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setCurrentEventCash', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    async getKitchenData() {
      const path = `${process.env.VUE_APP_API}basic/event/${this.eventId}/kitchen-eventmaster-overview/`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setCurrentEventKitchen', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    async getKitchenProgram() {
      const path = `${process.env.VUE_APP_API}basic/event/${this.eventId}/program-eventmaster-overview/`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setCurrentEventProgram', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
  },
};
</script>
