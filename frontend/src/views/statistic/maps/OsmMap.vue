<template>
  <v-container>
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <RegistrationFilter
                :eventId="eventId"
                @onFilterSelected="onFilterSelected"/>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row>
      <v-card style="height: 900px; width: 100%" class="top-margin">
        <l-map
            v-if="circles && circles.length > 0"
            :zoom="zoom"
            :center="center"
            :options="mapOptions"
            @update:center="centerUpdate"
            @update:zoom="zoomUpdate">
          <l-tile-layer :url="url" :attribution="attribution"/>
          <l-circle
              v-for="(circle, index) in circles"
              :lat-lng="getCoord(circle)"
              :radius="getRadius(circle)"
              :color="getColor(circle)"
              :key="index">
            <l-popup :content="createContent(circle)"/>
          </l-circle>
          <l-marker
              :v-if="eventLocation && eventLocation.location.zipCode"
              :lat-lng="[eventLocation.location.zipCode.lat, eventLocation.location.zipCode.lon]"
              color="green"
              :radius="10000">
            <l-popup content="Ungefährer Lagerplatz"/>
          </l-marker>
        </l-map>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { latLng } from 'leaflet';
import { LCircle, LMap, LPopup, LTileLayer } from 'vue2-leaflet'; //eslint-disable-line
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';

export default {
  mixins: [apiCallsMixin],
  name: 'Example',
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LCircle,
    RegistrationFilter,
  },
  data() {
    return {
      zoom: 6.5,
      radiusSlider: 2,
      center: latLng(51, 11),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      currentZoom: 5,
      currentCenter: latLng(51, 11),
      mapOptions: {
        zoomSnap: 0.5,
      },
      showMap: true,
      data: [],
      loading: false,
      eventLocation: null,
    };
  },
  computed: {
    circles() {
      if (this.selectedBookingOption) {
        return this.data.filter((item) => item.participantCount > 0);
      }
      return this.data;
    },
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(param) {
      this.loading = true;

      Promise.all([
        this.getEventLocationSummary(this.eventId),
        this.getRegistrationLocationsSummary(this.eventId, param),
      ])
        .then((values) => {
            this.data = values[1].data; //eslint-disable-line
            this.eventLocation = values[0].data[0];  //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(params) {
      this.getData(params);
    },
    getCoord(item) {
      if (item.scoutOrganisation.zipCode) {
        return [
          item.scoutOrganisation.zipCode.lat,
          item.scoutOrganisation.zipCode.lon,
        ];
      }
      const randomLat = Math.random() - 0.5;
      const randomLong = Math.random() - 0.5;
      return [54.181211 + randomLat, 7.899131 + randomLong];
    },
    getColor() {
      return 'blue';
    },
    getRadius() {
      return 100000 / (this.currentZoom * 2);
    },
    createContent(item) {
      let text = '';
      if (item.scoutOrganisation.bund) {
        text = `${item.scoutOrganisation.bund},`;
      }

      text = `${text} ${item.scoutOrganisation.name}`;

      if (item.scoutOrganisation.zipCode) {
        text = `${text} aus ${item.scoutOrganisation.zipCode.city}`;
      }
      return `${text}, Teilnehmer: ${item.participantCount}`;
    },
    zoomUpdate(zoom) {
      this.currentZoom = zoom;
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
  },
  mounted() {
    this.getData();
  },
};
</script>
