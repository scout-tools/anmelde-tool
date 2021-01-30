<template>
  <div>
    <GChart
      :settings="{
        packages: ['corechart', 'geochart'],
        mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850',
      }"
      type="GeoChart"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
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
      chartData: [],
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
  },
  methods: {
    json_to_chart_data(jsonData) {
      const returnData = [];
      debugger;
      jsonData.forEach((event) => {
        const buende = [];
        returnData.push([
          'Lat',
          'Lon',
          'Name',
          'Bund',
          'TN',
          { role: 'tooltip', p: { html: false } },
        ]);
        event.scoutOrganisations.forEach((loc) => {
          if (buende.indexOf(loc.bund) === -1) buende.push(loc.bund);
        });
        event.scoutOrganisations.forEach((loc) => {
          returnData.push([
            loc.lat,
            loc.lon,
            loc.scoutOrganisation_Name,
            buende.indexOf(loc.bund),
            loc.participants,
            `TN: ${loc.participants}\n Bund: ${loc.bund}`,
          ]);
        });
      });
      debugger;
      return returnData;
    },
    getData() {
      console.log(this.currentEventParticipants);
      this.chartData = this.json_to_chart_data(this.currentEventParticipants);
    },
  },
  created() {
    this.getData();
  },
};
</script>
