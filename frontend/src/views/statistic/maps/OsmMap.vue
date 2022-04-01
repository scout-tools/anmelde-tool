<template>
  <v-container class="top-margin">
    <v-row>
      <div style="height: 900px; width: 100%">
        <l-map
          v-if="data && data.length > 0"
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
            :key="index"
          >
            <l-popup :content="createContent(circle)"> </l-popup>
          </l-circle>
        </l-map>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import { latLng } from 'leaflet';

import { LMap, LTileLayer, LPopup, LCircle } from 'vue2-leaflet'; //eslint-disable-line

import serviceMixin from '@/mixins/serviceMixin';

export default {
  mixins: [serviceMixin],
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
      data: [],
    };
  },
  computed: {
    circles() {
      return this.data;
    },
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(eventId) {
      this.getRegistrationSummary(eventId).then((responseObj) => {
        this.data = responseObj.data[0].registrationSet;
      });
    },
    getCoord(item) {
      return [item.scoutOrganisation.zipCode.lat, item.scoutOrganisation.zipCode.lon];
    },
    getColor() {
      return 'blue';
    },
    getRadius() {
      return 100000 / (this.currentZoom * 2);
    },
    createContent(item) {
      console.log(item);
      return `${item.scoutOrganisation.bund},
        ${item.scoutOrganisation.name}
         aus ${item.scoutOrganisation.zipCode.city},
        Teilnehmer: ${item.participantCount}`;
    },
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
