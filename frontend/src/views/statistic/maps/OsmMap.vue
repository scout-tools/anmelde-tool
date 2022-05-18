<template>
  <v-container>
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <BookingFilter
                  :bookingOptionList="bookingOptionList"
                  :loading="loading"
                  @onFilterSelected="onFilterSelected"
                  v-model="selectedBookingOption"
                />
              </v-col>
            </v-row>
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
            :lat-lng="[data.location.zipCode.lat, data.location.zipCode.lon]"
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

import { LMap, LTileLayer, LPopup, LCircle } from 'vue2-leaflet'; //eslint-disable-line

import serviceMixin from '@/mixins/serviceMixin';
import BookingFilter from '@/components/common/BookingFilter.vue';

export default {
  mixins: [serviceMixin],
  name: 'Example',
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LCircle,
    BookingFilter,
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
      loading: false,
      bookingOptionList: [],
      selectedBookingOption: null,
    };
  },
  computed: {
    circles() {
      if (this.selectedBookingOption) {
        return this.data.registrationSet.filter((item) => item.participantCount > 0);
      }
      return this.data.registrationSet;
    },
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(eventId, param) {
      this.loading = true;

      Promise.all([
        this.getRegistrationSummary(eventId, param),
        this.getBookingOptions(eventId),
      ])
        .then((values) => {
          this.data = values[0].data[0]; //eslint-disable-line
          this.bookingOptionList = values[1].data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(values) {
      const params = new URLSearchParams();
      if (values) {
        values.forEach((value) => {
          params.append('booking-option', value);
        });
      }
      this.getData(this.eventId, params);
    },
    getCoord(item) {
      try {
        return [
          item.scoutOrganisation.zipCode.lat,
          item.scoutOrganisation.zipCode.lon,
        ];
      } catch (e) {
        console.log('Fehler');
        console.log(item);
        console.log(e);
        return [1, 1];
      }
    },
    getColor() {
      return 'blue';
    },
    getRadius() {
      return 100000 / (this.currentZoom * 2);
    },
    createContent(item) {
      try {
        return `${item.scoutOrganisation.bund},
        ${item.scoutOrganisation.name}
         aus ${item.scoutOrganisation.zipCode.city},
        Teilnehmer: ${item.participantCount}`;
      } catch (e) {
        console.log('Fehler');
        console.log(item);
        console.log(e);
        return '';
      }
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
