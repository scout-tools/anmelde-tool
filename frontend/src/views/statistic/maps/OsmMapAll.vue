<template>
  <v-container>
    <v-row>
      <template v-for="bund in bunde">
        <v-checkbox
          class="mx-2"
          :key="bund.id"
          v-model="selectedBunde"
          :color="bundColorObj[bund.bund]"
          :label="bund.bund"
          :value="bund.bund"
          v-if="bund.bund"
        ></v-checkbox>
      </template>
    </v-row>
    <v-row>
      <div style="height: 900px; width: 100%">
        <l-map
          v-if="circles && circles.length > 0"
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
            :fill="true"
            :fillColor="getColor(circle)"
            :fillOpacity="0.6"
            :key="index"
          >
            <l-popup :content="createContent(circle)"> </l-popup>
          </l-circle>
          <l-marker
            :lat-lng="getLonLatLocation()"
            color="green"
            :radius="10000"
          >
            <l-popup content="Ungefährer Lagerplatz"> </l-popup>
          </l-marker>
        </l-map>
      </div>
    </v-row>
  </v-container>
</template>

<script>
import { latLng } from 'leaflet';
import axios from 'axios';

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
      bundColorObj: {
        BEP: '#831ed',
        DPBM: '#007f4f',
        DPBH: '#393f4d',
        FPS: '#feda6a',
        Jomsburg: '#86cc52',
        'PB Boreas': '#00DDFF',
        'PB-Horizonte': '#e62739',
        'PB-Nordlicht': '#8076f5',
        PBMV: '#ff1d58',
        PBN: '#88dbb4',
        PBW: '#fbaf08',
        PSD: '#0f2862',
      },
      selectedBunde: [],
      summary: [],
    };
  },
  computed: {
    circles() {
      return this.data
        .filter((item) => item.level === 'Stamm')
        .filter((item) => this.selectedBunde.includes(item.bund));
    },
    bunde() {
      return this.data.filter((item) => item.abbreviation !== null);
    },
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getLonLatLocation() {
      debugger;
      try {
        return [
          this.summary.location.zipCode.lat,
          this.summary.location.zipCode.lon,
        ];
      } catch (e) {
        console.log('Fehler');
        return [1, 1];
      }
    },
    randomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    },

    async getHierarchyMapping() {
      const path = `${process.env.VUE_APP_API}/basic/scout-hierarchy/`;
      const response = await axios.get(path);

      return response.data;
    },
    getData() {
      this.getHierarchyMapping().then((responseObj) => {
        this.data = responseObj; // eslint-disable-line
      });
      this.getRegistrationSummary(this.eventId).then((responseObj) => {
        this.summary = responseObj.data[0]; // eslint-disable-line
      });
    },
    getCoord(item) {
      try {
        return [item.zipCode.lat, item.zipCode.lon];
      } catch (e) {
        console.log('Fehler');
        console.log(item);
        console.log(e);
        return [1, 1];
      }
    },
    getColor(item) {
      return this.bundColorObj[item.bund];
    },
    getRadius() {
      return 70000 / (this.currentZoom * 2);
    },
    createContent(item) {
      try {
        return `${item.bund},
        ${item.name}
         aus ${item.zipCode.city}`;
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
    this.selectedBunde = Object.keys(this.bundColorObj);
    this.getData();
  },
};
</script>
