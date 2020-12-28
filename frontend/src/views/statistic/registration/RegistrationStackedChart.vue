<template>
  <GChart
    :settings="{
      packages: ['corechart'],
      mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850',
    }"
    type="SteppedAreaChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import Vue from 'vue';
import VueGoogleCharts, { GChart } from 'vue-google-charts';
import { EventBus } from '@/main';

Vue.use(VueGoogleCharts);

export default {
  name: 'RegistrationStackedChart',
  components: {
    GChart,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartData: [
        ['date', 'number'],
        [new Date(2020, 9, 4), 100],
        [new Date(2020, 9, 5), 200],
        [new Date(2020, 9, 12), 250],
        [new Date(2020, 9, 13), 300],
        [new Date(2020, 9, 19), 300],
        [new Date(2020, 9, 23), 300],
        [new Date(2020, 9, 24), 500],
        [new Date(2020, 9, 30), 1000],
      ],
      chartOptions: {
        title: 'Anmedlungen',
        isStacked: true,
        width: 800,
        height: 600,
        legend: { position: 'right', maxLines: 3 },
        vAxis: { minValue: 0 },
      },
    };
  },
  mounted() {
    EventBus.$on('newParticipantsData', (participantsData) => {
      this.chartData = this.json_to_chart_data(participantsData);
    });
  },
  beforeDestroy() {
    EventBus.$off('newParticipantsData');
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      const buende = [];
      jsonData.forEach((regis) => {
        if (buende.indexOf(regis.bund) === -1) buende.push(regis.bund);
      });
      chartData.push(['date'].concat(buende));
      jsonData.forEach((regis) => {
        // eslint-disable-next-line no-param-reassign
        regis.createdAt = new Date(regis.createdAt);
      });
      jsonData.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());

      const buendeCount = new Array(buende.length).fill(0);
      jsonData.forEach((regis) => {
        buendeCount[buende.indexOf(regis.bund)] += regis.numberOfPersons;
        chartData.push([regis.createdAt].concat(buendeCount));
      });
      return chartData;
    },
  },
};
</script>
