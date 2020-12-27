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
import VueGoogleCharts, { GChart } from 'vue-google-charts';
import axios from 'axios';

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
    const jsonData = this.getTestData();
    console.log(this.chartData);
    this.chartData = this.json_to_chart_data(jsonData);
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
      jsonData.registrations.forEach((regis) => {
        if (buende.indexOf(regis.bund) === -1) buende.push(regis.bund);
      });
      jsonData.registrations.forEach((regis) => {
        chartData.push([
          regis.laz,
          regis.long,
          regis.name,
          buende.indexOf(regis.bund),
          regis.tn_count,
          `TN: ${regis.tn_count}\n Bund: ${regis.bund}`,
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
          },
          {
            bund: 'PB-Nordlicht',
            name: 'Anduril',
            tn_count: 20,
            long: 10.4115179,
            laz: 53.2464214,
          },
          {
            bund: 'PB-Nord',
            name: 'Ambronen',
            tn_count: 30,
            long: 9.993682,
            laz: 53.551085,
          },
          {
            bund: 'Andere Pfadis',
            name: 'Heruler',
            tn_count: 150,
            long: 13.404954,
            laz: 52.520007,
          },
        ],
      };
      return data;
    },
    getData() {
      const path = `${this.API_URL}basic/statistic/map/22`;
      axios
        .get(path)
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
