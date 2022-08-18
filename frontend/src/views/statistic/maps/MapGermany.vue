<template>
  <div>
    <GChart
      :settings="{
        packages: ['corechart', 'geochart'],
        mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850',
      }"
      type="GeoChart"
      :data="charData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import { GChart } from 'vue-google-charts';

export default {
  mixins: [apiCallsMixin],
  components: {
    GChart,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      data: [],
      chartOptions: {
        region: 'DE',
        displayMode: 'markers',
        colorAxis: { colors: ['blue', 'red'] },
        resolution: 'provinces',
        tooltip: {
          isHtml: false,
        },
        height: 500,
        legend: false,
      },
    };
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    charData() {
      const returnData = [];
      returnData.push([
        'Lat',
        'Lon',
        'Name',
      ]);

      this.data.forEach((loc) => {
        try {
          returnData.push([
            parseFloat(loc.scoutOrganisation.zipCode.lat),
            parseFloat(loc.scoutOrganisation.zipCode.lon),
            loc.scoutOrganisation.name,
          ]);
        } catch (e) {
          console.log('Fehler');
          console.log(loc);
          console.log(e);
        }
      });
      return returnData;
    },
  },
  methods: {
    getData() {
      this.getRegistrationLocationsRegistrationSummary(this.eventId).then((responseObj) => {
        this.data = responseObj.data;
      });
    },
  },
  created() {
    this.getData();
  },
};
</script>
