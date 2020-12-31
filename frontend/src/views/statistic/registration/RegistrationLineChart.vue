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
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationLineChart',

  data() {
    return {
      API_URL: process.env.VUE_APP_API,
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
  computed: {
    ...mapGetters(['currentEventParticipants']),
    chartData() {
      return this.json_to_chart_data(this.currentEventParticipants);
    },
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
