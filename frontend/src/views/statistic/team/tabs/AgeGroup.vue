<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <RegistrationFilter
                  :eventId="eventId"
                  @onFilterSelected="onFilterSelected"/>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-card flat v-if="!loading">
        <apexchart
            width="500"
            type="bar"
            :options="options"
            :series="series"/>
      </v-card>
      <v-card v-else flat>
        <div class="text-center ma-5">
          <p>Lade Daten ...</p>
          <v-progress-circular
              :size="80"
              :width="10"
              class="ma-5"
              color="primary"
              indeterminate/>
          <p>Bitte hab etwas Geduld.</p>
        </div>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>

import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
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
  }),
  methods: {
    getString(key) {
      return this.mapping[key];
    },
    getData(params) {
      this.loading = true;

      this.getEventAgeGroups(this.eventId, params)
        .then((result) => {
            this.data = result.data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(params) {
      this.getData(params);
    },
  },
  created() {
    this.getData(null);
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    ageGroups() {
      if (this.data) {
        return this.data;
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
