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
import VueGoogleCharts, {GChart} from 'vue-google-charts';
import {EventBus} from '@/main';

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
      chartData.push(['date', 'number']);
      jsonData.forEach((regis) => {
        chartData.push([
          new Date(regis.createdAt),
          regis.numberOfPersons,
        ]);
      });
      return chartData;
    },
  },
};
</script>
