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
import VueGoogleCharts, { GChart } from 'vue-google-charts';
import axios from 'axios';

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
    const jsonData = this.getTestData();
    this.chartData = this.json_to_chart_data(jsonData);
    console.log(this.chartData);
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      chartData.push(['date', 'number']);
      jsonData.registrations.forEach((regis) => {
        // eslint-disable-next-line no-param-reassign
        regis.date = new Date(regis.date);
      });
      jsonData.registrations.sort((a, b) => a.date.getTime() - b.date.getTime());

      let count = 0;
      jsonData.registrations.forEach((regis) => {
        count += regis.tn_count;
        chartData.push([
          regis.date,
          count,
        ]);
      });
      return chartData;
    },
    getTestData() {
      const data = {
        registrations: [
          {
            bund: 'PB-Nordlicht',
            name: 'Ambronen',
            tn_count: 200,
            long: 9.993682,
            laz: 53.551085,
            date: new Date(2020, 2, 22).toString(),
          },
          {
            bund: 'PB-Nordlicht',
            name: 'Anduril',
            tn_count: 20,
            long: 10.4115179,
            laz: 53.2464214,
            date: new Date(2020, 2, 23).toString(),
          },
          {
            bund: 'PB-Nord',
            name: 'Ambronen',
            tn_count: 30,
            long: 9.993682,
            laz: 53.551085,
            date: new Date(2020, 3, 4).toString(),
          },
          {
            bund: 'Andere Pfadis',
            name: 'Heruler',
            tn_count: 150,
            long: 13.404954,
            laz: 52.520007,
            date: new Date(2020, 3, 20).toString(),
          },
        ],
      };
      return data;
    },
    getData() {
      const path = `${this.API_URL}basic/statistic/map/22`;
      axios.get(path)
        .then((res) => {
          this.chartData = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
  },
};
</script>
