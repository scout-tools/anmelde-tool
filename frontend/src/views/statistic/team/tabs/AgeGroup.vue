<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <v-autocomplete
                  clearable
                  :loading="loading"
                  :items="bookingOptionList"
                  v-model="selectedBookingOption"
                  label="Filter nach Buchoptionen"
                  item-text="name"
                  item-value="id"
                  @change="onFilterSelected"
                  no-data-text="Keine Buchoptionen gefunden."/>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <apexchart
        width="500"
        type="bar"
        :options="options"
        :series="series"/>
    </v-row>
  </v-container>
</template>

<script>

import serviceMixin from '@/mixins/serviceMixin';

export default {
  mixins: [serviceMixin],
  data: () => ({
    data: [],
    mapping: {
      woelfling: 'Wölfling (bis 10)',
      pfadfinder: 'Pfadfinder (11-16)',
      rover: 'Rover (17-23)',
      altRover: 'Altrover (24+)',
    },
    loading: false,
    bookingOptionList: [],
    selectedBookingOption: null,
  }),
  methods: {
    getString(key) {
      return this.mapping[key];
    },
    getData(eventId, param) {
      this.loading = true;

      Promise.all([
        this.getRegistrationSummary(eventId, param),
        this.getBookingOptions(eventId),
      ])
        .then((values) => {
          this.data = values[0].data; //eslint-disable-line
          this.bookingOptionList = values[1].data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(value) {
      const params = new URLSearchParams();
      if (value) {
        params.append('booking-option', value);
      }
      this.getData(this.eventId, params);
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
