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
    ...mapGetters(['currentEventKitchen']),

  },

  methods: {
    json_to_chart_data(jsonData) {
      const returnData = [];
      returnData.push(['Type', 'Number']);
      jsonData.forEach((event) => {
        returnData.push(['Vegetarier', event.numVegetarien.veggiPersonal]);
        returnData.push(['Veganer', event.numVegan.veganPersonal]);
        returnData.push(['Omnivor', event.totalParticipants - event.numVegan.veganPersonal - event.numVegetarien.veggiPersonal]);
      });
      return returnData;
    },
    getData() {
      this.chartData = this.json_to_chart_data(this.currentEventKitchen);
    },
  },
  created() {
    this.getData();
  },
};
</script>
