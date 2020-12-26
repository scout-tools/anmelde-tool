<template>
  <v-container>
    <v-row justify="center">
      <v-flex
        ma-3
        lg9
      >
    <v-layout column>
  <v-container fluid>
    <v-row align="center">
      <v-col
        class="d-flex"
        cols="12"
        sm="6"
      >
        <v-select
          :items="getItems"
          label="Wähle eine Veranstaltung aus..."
          v-model="selected"
          item-value="id"
          item-text="name"
          dense
        ></v-select>
      </v-col>
    </v-row>
  </v-container>
      <v-card :disabled="!selected">
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
        Übersicht
        <v-icon>mdi-poll</v-icon>
      </v-tab>

      <v-tab href="#tab-2">
        Anmeldungen
        <v-icon>mdi-counter</v-icon>
      </v-tab>

      <v-tab href="#tab-3">
        Karte
        <v-icon>mdi-map</v-icon>
      </v-tab>

      <v-tab href="#tab-4">
        Diagramme
        <v-icon>mdi-chart-line</v-icon>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="i in 4"
        :key="i"
        :value="'tab-' + i"
      >
        <v-card-text>
          <summary-main v-if="i === 1"/>
          <registration-main v-if="i === 2"/>
          <maps-main v-if="i === 3"/>
          <diagramms-main v-if="i === 4"/>
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
import SummaryMain from '@/views/statistic/summary/Main.vue';
import RegistrationMain from '@/views/statistic/registration/Main.vue';
import DiagrammsMain from '@/views/statistic/diagramms/Main.vue';

export default {
  components: {
    MapsMain,
    SummaryMain,
    RegistrationMain,
    DiagrammsMain,

  },
  data() {
    return {
      tab: null,
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
      items: null,
      selected: null,
    };
  },
  computed: {
    getItems() {
      return this.items;
    },
  },
  methods: {
    getData() {
      const path = `${process.env.VUE_APP_API}basic/event/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data;
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
