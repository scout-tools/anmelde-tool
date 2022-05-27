<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="4">
                <v-checkbox
                  v-model="filter.justConfirmed"
                  label="Nur Bestätigt"
                  hide-details
                ></v-checkbox>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
        :headers="headers"
        :items="getItems"
        :items-per-page="itemsPerPage"
        :expanded.sync="expanded"
        hide-default-footer
        :item-class="rowClasses"
      >
        <template v-slot:[`item.isConfirmed`]="{ item }">
          <v-icon :color="item.isConfirmed ? 'green' : 'red'">
            {{
              item.isConfirmed ? 'mdi-check-circle' : 'mdi-close-circle'
            }}</v-icon
          >
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ moment(item.createdAt).format('DD.MM.YYYY') }}
        </template>
        <template v-slot:[`item.numberParticipant`]="{ item }">
          <td v-html="getNumberParticipant(item)" disabled></td>
        </template>
        <template v-slot:[`item.price`]="{ item }">
          <td v-html="getPrice(item)"></td>
        </template>
        <template v-slot:expanded-item="{ item }">
          <td :colspan="headers.length">
            <pre>{{ getBody(item) }}</pre>
          </td>
        </template>
        <template slot="body.append">
          <tr>
            <th>Summe</th>
            <th colspan="3">{{ getTotalStamm }}</th>
            <th>{{ getTotalParticipant }}</th>
          </tr>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment'; // eslint-disable-line

export default {
  mixins: [apiCallsMixin],
  data: () => ({
    data: [],
    expanded: [],
    filter: {
      justConfirmed: false,
    },
    headers: [
      { text: 'Bestätigt', value: 'isConfirmed' },
      { text: 'Datum', value: 'createdAt' },
      { text: 'Bund', value: 'scoutOrganisation.bund' },
      { text: 'Name', value: 'scoutOrganisation.name' },
      { text: 'Gesamtpreis', value: 'price' },
      { text: '', value: 'data-table-expand' },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    getItems() {
      const data = this.data.filter(
        (item) =>
          item.isConfirmed === this.filter.justConfirmed || // eslint-disable-line
          !this.filter.justConfirmed,
      );
      return data;
    },
    getTotalParticipant() {
      const price = this.getItems.reduce(
        (accum, item) => accum + item.price,
        0,
      ); // eslint-disable-line
      return `${price || 0} €`;
    },
    getTotalStamm() {
      const numberStammBdp = this.getItems.length;
      return `Stämme ${numberStammBdp || 0}`;
    },
  },

  methods: {
    getBody(item) {
      return item.tags;
    },
    getPrice(item) {
      return item.price ? `${item.price} €` : '0 €';
    },
    rowClasses(item) {
      if (item.verbandName === 'DPV') {
        return 'dpv-blue';
      }
      return 'bdp-yellow';
    },
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0} (${item.numberHelper || 0})`;
    },
    getData(eventId) {
      this.getRegistrationSummary(eventId).then((responseObj) => {
        this.data = responseObj.data[0].registrationSet;
      });
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>

<style>
.dpv-blue {
  background-color: rgba(56, 117, 238, 0.082);
}
.bdp-yellow {
  background-color: #ffcc0227;
}
</style>
