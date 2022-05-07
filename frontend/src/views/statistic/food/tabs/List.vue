<template>
  <v-container fluid class="pa-0">
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
        :headers="headers"
        :items="data"
        :items-per-page="itemsPerPage"
        hide-default-footer>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment'; // eslint-disable-line

export default {
  mixins: [serviceMixin],
  data: () => ({
    headers: [
      { text: 'Besonderheit', value: 'food' },
      { text: 'Personenanzahl', value: 'sum' },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    data: [],
    itemsPerPage: 1000,
  }),

  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(eventId) {
      this.getFoodSummary(eventId)
        .then((responseObj) => {
        this.data = responseObj.data.eatHabitsDetailed; // eslint-disable-line
        });
    },
  },
  mounted() {
    this.getData(this.eventId);
  },
};
</script>
