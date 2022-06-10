<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <RegistrationFilter
                :bookingOptionList="bookingOptionList"
                :loading="loading"
                @onFilterSelected="onFilterSelected"
                :justConfirmed="justConfirmed"/>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
          :headers="headers"
          :items="data"
          :items-per-page="itemsPerPage"
          hide-default-footer
          no-data-text="Keine Teilnehmer.">
      </v-data-table>
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
    headers: [
      {
        text: 'Besonderheit',
        value: 'food',
      },
      {
        text: 'Personenanzahl',
        value: 'sum',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    data: [],
    itemsPerPage: 1000,
    loading: false,
    bookingOptionList: [],
    selectedBookingOption: null,
    justConfirmed: true,
  }),

  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(param) {
      this.loading = true;

      Promise.all([
        this.getFoodSummary(this.eventId, param),
        this.getBookingOptions(this.eventId),
      ])
        .then((values) => {
            this.data = values[0].data; //eslint-disable-line
            this.bookingOptionList = values[1].data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(param) {
      this.getData(param);
    },
  },
  mounted() {
    this.getData(this.eventId, null);
  },
};
</script>
