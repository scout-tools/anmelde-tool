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
import Vue from 'vue';
import VueGoogleCharts, {GChart} from 'vue-google-charts';
import {EventBus} from '@/main';

Vue.use(VueGoogleCharts);

export default {
  components: {
    GChart,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartData: [
        [
          'Laz',
          'Long',
          'Name',
          'Bund',
          'Gruppen',
          { role: 'tooltip', p: { html: true } },
        ],
        [52.520008, 13.404954, 'Berlin', 1, 4, '<h3>TEST</h3> 4t34t 4hreg '],
        [53.551085, 9.993682, 'Hamburg', 2, 6, 'efeg'],
        [53.551185, 9.393682, 'Lüneburg', 1, 1, 'eqpm'],
      ],
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
  mounted() {
    EventBus.$on('newParticipantsData', (participantsData) => {
      this.chartData = this.json_to_chart_data(participantsData);
    });
    EventBus.$emit('requestNewParticipantsData', this.participantsData);
  },
  beforeDestroy() {
    EventBus.$off('newParticipantsData');
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      const buende = [];
      chartData.push([
        'Laz',
        'Long',
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
