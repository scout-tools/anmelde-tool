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
import { mapGetters } from 'vuex';

export default {
  name: 'RegistrationCalender',
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      chartOptions: {
        colorAxis: { colors: ['blue', 'red'] },
        title: 'Anmeldungen',
        height: 350,

      },
      chartEvents: {
        select: () => {
          const table = this.$refs.gChart.chartObject;
          const selection = table.getSelection();
          const onSelectionMessage = selection.length !== 0 ? 'row was selected' : 'row was diselected';
          alert(onSelectionMessage);
        },
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
