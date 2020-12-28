<template>
  <GChart
    :settings="{
        packages: ['corechart', 'line'],
        mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850'
      }"
    type="LineChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>
import Vue from 'vue';
import VueGoogleCharts, {GChart} from 'vue-google-charts';
import {EventBus} from '@/main';

Vue.use(VueGoogleCharts);

export default {
  name: 'RegistrationLineChart',
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
        curveType: 'function',
        width: 800,
        height: 600,
        legend: { position: 'right' },
        vAxis: { minValue: 0 },
      },
    };
  },
  mounted() {
    EventBus.$on('newParticipantsData', (participantsData) => {
      this.chartData = this.json_to_chart_data(participantsData);
    });
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      chartData.push(['date', 'number']);
      jsonData.forEach((regis) => {
        // eslint-disable-next-line no-param-reassign
        regis.createdAt = new Date(regis.createdAt);
      });
      jsonData.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());

      let count = 0;
      jsonData.forEach((regis) => {
        count += regis.numberOfPersons;
        chartData.push([
          regis.createdAt,
          count,
        ]);
      });
      return chartData;
    },
  },
};
</script>
