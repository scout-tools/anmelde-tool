<template>
  <v-container class="top-margin">
    <v-row>
    <div style="height: 900px; width: 100%">
    <l-map
      :zoom="zoom"
      :center="center"
      :options="mapOptions"
      @update:center="centerUpdate"
      @update:zoom="zoomUpdate"
    >
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-circle
        v-for="(circle, index) in circles"
        :lat-lng="getCoord(circle)"
        :radius="getRadius(circle)"
        :color="getColor(circle)"
        :key="index">
        <l-popup :content="createContent(circle)">
        </l-popup>
      </l-circle>
    </l-map>
    </div>
    </v-row>
    <v-divider class="my-6"/>
    <v-row>
      <v-col cols="8" sm="8">
    <v-slider
      v-model="radiusSlider"
      color="black"
      label="Radius in km"
      min=10
      max="250"
      thumb-label="always"
    >
    </v-slider>
      </v-col>
        <v-col cols="4" sm="4">
        <p>
        Zoom {{ this.currentZoom }}
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { latLng } from 'leaflet';
import { mapGetters } from 'vuex';

import {
  LMap,
  LTileLayer,
  LPopup,
  LCircle,
} from 'vue2-leaflet';

export default {
  name: 'Example',
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LCircle,
  },
  data() {
    return {
      zoom: 6.5,
      radiusSlider: 2,
      center: latLng(51, 11),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 5,
      currentCenter: latLng(51, 11),
      mapOptions: {
        zoomSnap: 0.5,
      },
      showMap: true,
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
    circles() {
      return this.currentEventParticipants[0].scoutOrganisations;
    },
  },
  methods: {
    getCoord(item) {
      return [item.lat, item.lon];
    },
    getColor(item) {
      return item.bund === 'BdP' ? 'red' : 'blue';
    },
    getRadius() {
      return this.radiusSlider * 1000;
    },
    createContent(item) {
      return `${item.bund},
        ${item.scoutOrganisation_Name}
         aus ${item.city},
        Auswahl: ${item.choice},
        Teilnehmer: ${item.participants}`;
    },
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
  },
};
</script>
