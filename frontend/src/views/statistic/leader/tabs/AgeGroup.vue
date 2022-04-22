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
import axios from 'axios';

export default {
  data: () => ({
    data: [],
    mapping: {
      woelfling: 'Wölfling',
      jungPfadfinder: 'Jungpfadfinder',
      pfadfinder: 'Pfadfinder',
      rover: 'Rover',
      altRover: 'Altrover',
    },
  }),
  methods: {
    getString(key) {
      return this.mapping[key];
    },
    getData(eventId) {
      this.getRegistrationSummary(eventId).then((responseObj) => {
        this.data = responseObj.data;
      });
    },
    async getRegistrationSummary(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/`;
      return axios.get(path);
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
          data: Object.keys(this.mapping).map((item) => {
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
