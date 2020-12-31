<template>
  <v-container>
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-container fluid class="ma-6">
            <v-row align="center">
              <v-col class="d-flex" cols="12" sm="6">
                <v-select
                  :items="getItems"
                  label="Wähle eine Veranstaltung aus..."
                  v-model="selected"
                  item-value="id"
                  item-text="name"
                  @change="changedEvent"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
          <v-card v-if="selected">
            <v-tabs
              v-model="tab"
              background-color="primary"
              grow
              centered
              dark
              icons-and-text
              :disabled="!items"
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
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="i in 4" :key="i" :value="'tab-' + i">
                <v-card-text>
                  <registration-main v-if="i === 1" />
                  <maps-main v-if="i === 2" />
                  <cash-main v-if="i === 3" />
                  <kitchen-main v-if="i === 4" />
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
import KitchenMain from '@/views/statistic/kitchen/Main.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    MapsMain,
    RegistrationMain,
    CashMain,
    KitchenMain,
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
    getItems() {
      return this.items;
    },
  },
  data() {
    return {
      tab: null,
      items: [],
      selected: null,
    };
  },
  methods: {
    changedEvent() {
      if (typeof this.selected === 'number') {
        this.getParticipantsData(this.selected);
      }
    },
    getData() {
      const path = `${process.env.VUE_APP_API}basic/event/`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    getParticipantsData(eventId) {
      const path = `${process.env.VUE_APP_API}basic/event/${eventId}/participants/`;
      axios.get(path)
        .then((res) => {
          this.$store.commit('setCurrentEventParticipants', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
