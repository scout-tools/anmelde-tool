<template>
  <v-container class="top-margin">
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
        DPBM: '#93f1e5',
        DPBH: '#eec1c',
        FPS: '#995aec',
        Jomsburg: '#86cc52',
        'PB Boreas': '#272531',
        'PB-Horizonte': '#8abc46',
        'PB-Nordlicht': '#8076f5',
        PBMV: '#eb78f6',
        PBN: '#88dbb4',
        PBW: '#4bff6e',
        PSD: '#bbab37',
      },
    };
  },
  computed: {
    circles() {
      return this.data.filter((item) => item.level === 'Stamm');
    },
    bunde() {
      return this.data.filter((item) => item.abbreviation !== null);
    },
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    randomColor() {
      return `#${Math.floor(Math.random() * 16777215).toString(16)}`;
    },

    async getHierarchyMapping() {
      const path = `${process.env.VUE_APP_API}/basic/scout-hierarchy/`;
      debugger;
      const response = await axios.get(path);

      return response.data;
    },
    getData() {
      this.getHierarchyMapping().then((responseObj) => {
        this.data = responseObj; // eslint-disable-line
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
    this.getData();
  },
};
</script>
