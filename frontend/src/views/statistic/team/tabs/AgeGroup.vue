<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <BookingFilter
                  :bookingOptionList="bookingOptionList"
                  :loading="loading"
                  @onFilterSelected="onFilterSelected"
                  v-model="selectedBookingOption"
                />
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

import apiCallsMixin from '@/mixins/apiCallsMixin';
import BookingFilter from '@/components/common/BookingFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    BookingFilter,
  },
  data: () => ({
    data: [],
    mapping: {
      woelfling: 'Wölfling (bis 12)',
      pfadfinder: 'Pfadfinder (13-17)',
      rover: 'Rover (18-24)',
      altRover: 'Altrover (25+)',
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
        this.getEventAgeGroups(eventId, param),
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
    onFilterSelected(values) {
      const params = new URLSearchParams();
      if (values) {
        values.forEach((value) => {
          params.append('booking-option', value);
        });
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
