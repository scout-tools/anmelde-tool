<template>
  <GChart
    :settings="{
        packages: ['corechart', 'calendar'],
        mapsApiKey: 'AIzaSyA8b79CjjX-C9VgxMBF2aTs9fOI-UBT850'
      }"
    type="Calendar"
    :data="chartData"
    :options="chartOptions"
    :events="chartEvents"
    ref="gChart"
  />
</template>

<script>
import Vue from 'vue';
import VueGoogleCharts, { GChart } from 'vue-google-charts';
import axios from 'axios';

Vue.use(VueGoogleCharts);

export default {
  name: 'RegistrationCalender',
  components: {
    GChart,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartData: [
        ['date', 'number'],
        [new Date(2013, 9, 4), 38177],
        [new Date(2013, 9, 5), 38705],
        [new Date(2013, 9, 12), 38210],
        [new Date(2013, 9, 13), 38029],
        [new Date(2013, 9, 19), 38823],
        [new Date(2013, 9, 23), 38345],
        [new Date(2013, 9, 24), 38436],
        [new Date(2013, 9, 30), 38447],
      ],
      chartOptions: {
        colorAxis: { colors: ['blue', 'red'] },
        title: 'Anmeldungen',
        height: 350,

      },
      chartEvents: {
        select: () => {
          const table = this.$refs.gChart.chartObject;
          const selection = table.getSelection();
          const onSelectionMeaasge = selection.length !== 0 ? 'row was selected' : 'row was diselected';
          alert(onSelectionMeaasge);
        },
      },
    };
  },
  mounted() {
    const jsonData = this.getTestData();
    console.log(this.chartData);
    this.chartData = this.json_to_chart_data(jsonData);
  },
  methods: {
    json_to_chart_data(jsonData) {
      const chartData = [];
      const buende = [];
      chartData.push(['date', 'number']);
      jsonData.registrations.forEach((regis) => {
        chartData.push([
          new Date(regis.date),
          regis.tn_count,
        ]);
      });
      console.log(buende);
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
