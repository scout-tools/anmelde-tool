<template>
  <div>
    <GChart
      type="ColumnChart"
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>

export default {
  data() {
    return {
      chartDataHeader: ['Wölflinge', 'Pfadfinder', 'Rover', 'Altrover'],
      chartDataRows: [
        ['Vegan', 5, 20, 7],
        ['Vegetarisch', 40, 100, 18],
        ['Fleisch', 100, 200, 100],
      ],
      chartOptions: {
        chart: {
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
