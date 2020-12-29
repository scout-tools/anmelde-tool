<template>
  <div class="about">
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
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
    chartData() {
      return this.json_to_chart_data(this.currentEventParticipants);
    },
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      const buende = [];
      chartData.push([
        'Lat',
        'Lon',
        'Name',
        'Bund',
        'TN',
        { role: 'tooltip', p: { html: false } },
      ]);
      jsonData.forEach((regis) => {
        if (buende.indexOf(regis.bund) === -1) buende.push(regis.bund);
      });
      jsonData.forEach((regis) => {
        chartData.push([
          regis.lat,
          regis.lon,
          regis.name,
          buende.indexOf(regis.bund),
          regis.numberOfPersons,
          `TN: ${regis.numberOfPersons}\n Bund: ${regis.bund}`,
        ]);
      });
      return chartData;
    },
  },
};
</script>
