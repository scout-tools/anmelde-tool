<template>
    <GChart
      type="Table"
      :data="chartData"
      :options="chartOptions"
    />
</template>

<script>

export default {
  data() {
    return {
      chartDataHeader: ['', 'Gesamt', 'Wölflinge', 'Pfadfinder', 'Rover', 'Altrover'],
      chartDataRows: [
        ['Gesamt', 100, 10, 20, 7, 0],
        ['Fleisch', 100, 8, 18, 6, 0],
        ['Vegetarisch', 100, 1, 1, 1, 0],
        ['Vegan', 100, 0, 1, 0, 0],
        ['Keine Nüße', 100, 0, 0, 0, 0],
      ],
      updatedChartData: [],
      chartOptions: {
        table: {
          title: 'Company Performance',
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
