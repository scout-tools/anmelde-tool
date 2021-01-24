<template>
  <GChart
    type="Table"
    :data="chartData"
    :options="chartOptions"
  />
</template>

<script>

import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      chartDataHeader: ['', 'Gesamt', 'Wölflinge', 'Pfadfinder', 'Rover', 'Altrover'],
      chartDataRows: [
        ['Gesamt', 100, 10, 20, 7, 0],
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
    ...mapGetters(['currentEventProgram']),

  },

  methods: {
    json_to_chart_data(jsonData) {
      const returnData = [];
      returnData.push(['Altersgruppe', 'Group TN', 'Single TN', 'TN']);
      jsonData.forEach((event) => {
        event.participantsGroupedByAge.forEach((group) => {
          returnData.push([
            group.ageGroup,
            group.numberGroup,
            group.numberPersonal,
            group.numberGroup + group.numberPersonal,
          ]);
        });
      });
      return returnData;
    },
    getData() {
      this.chartData = this.json_to_chart_data(this.currentEventProgram);
    },
  },
  created() {
    this.getData();
  },
};
</script>
