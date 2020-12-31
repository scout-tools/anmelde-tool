<template>
  <GChart
    type="PieChart"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>

export default {
  data() {
    return {
      chartDataHeader: ['Fleischgewohnheit', 'Anzahl'],
      chartDataRows: [
        ['Vegan', 11],
        ['Vegetarisch', 2],
        ['Fleisch', 2],
      ],
      chartOptions: {
        title: 'Fleischgewohnheiten',
        legend: {
          position: 'right',
        },
      },
    };
  },

  computed: {
    chartData() {
      return [this.chartDataHeader, ...this.chartDataRows];
    },
  },
};
</script>
