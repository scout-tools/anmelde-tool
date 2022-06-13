<template>
  <div>
    <apexchart
      width="500"
      type="bar"
      :options="options"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  data: () => ({
    data: [],
    mapping: {
      woelfling: 'Wölfling (bis 10)',
      pfadfinder: 'Pfadfinder (11-16)',
      rover: 'Rover (17-23)',
      altRover: 'Altrover (24+)',
    },
  }),
  methods: {
    getString(key) {
      return this.mapping[key];
    },
    getData(eventId) {
      this.getEventSummary(eventId)
        .then((responseObj) => {
          this.data = responseObj.data;
        });
    },
  },
  created() {
    this.getData(this.eventId);
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    ageGroups() {
      if (this.data && this.data[0]) {
        return this.data[0].ageGroups;
      }
      return [];
    },
    options() {
      return {
        chart: {
          type: 'bar',
          height: 500,
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          categories: Object.values(this.mapping),
        },
      };
    },
    series() {
      return [
        {
          name: 'Personen',
          data: Object.keys(this.mapping)
            .map((item) => {
              if (this.ageGroups && this.ageGroups.length === 0) {
                return 0;
              }
              return this.ageGroups[item];
            }),
        },
      ];
    },
  },
};
</script>

<style>
</style>
