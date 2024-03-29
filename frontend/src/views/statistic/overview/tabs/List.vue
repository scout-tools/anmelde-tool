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
              <!-- <v-col cols="4">
                <v-checkbox
                  v-model="filter.withBdp"
                  label="BdP"
                  hide-details
                ></v-checkbox>
              </v-col>
              <v-col cols="4">
                <v-checkbox
                  v-model="filter.withDpv"
                  label="DPV"
                  hide-details
                ></v-checkbox>
              </v-col> -->
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
          {{
            getDateFormat(item.createdAt)
          }}
        </template>
        <template v-slot:[`item.numberParticipant`]="{ item }">
          <td v-html="getNumberParticipant(item)" disabled></td>
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
import axios from 'axios';
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment'; // eslint-disable-line

export default {
  mixins: [serviceMixin],
  data: () => ({
    data: [],
    expanded: [],
    filter: {
      withDpv: true,
      withBdp: true,
      justConfirmed: false,
    },
    headers: [
      { text: 'Bestätigt', value: 'isConfirmed' },
      { text: 'Datum', value: 'createdAt' },
      { text: 'Bund', value: 'bundName' },
      { text: 'Name', value: 'scoutOrganisation' },
      { text: 'Teilnehmende', value: 'numberParticipant' },
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
    getItems() {
      return this.data;
    },
    getTotalParticipant() {
      const numberParticipant = this.getItems.reduce(
        (accum, item) => accum + item.numberParticipant,
        0,
      ); // eslint-disable-line
      const numberHelper = this.getItems.reduce(
        (accum, item) => accum + item.numberHelper,
        0,
      );

      return `${numberParticipant || 0} (${numberHelper || 0})`;
    },
    getTotalStamm() {
      const numberStammDpv = this.getItems.filter((item) => item.verbandName === 'DPV').length;
      const numberStammBdp = this.getItems.filter((item) => item.verbandName === 'BdP').length;

      return `Stämme DPV: ${numberStammDpv || 0} - Stämme BdP:${numberStammBdp || 0}`;
    },
  },

  methods: {
    getBody(item) {
      return `Stadt: ${item.stammCity}\nVerantwortlich: ${JSON.stringify(
        item.responsiblePersons,
      )
        .replaceAll('","', '\n\t')
        .replaceAll('[{"', '\n\t')}`;
    },
    rowClasses(item) {
      if (item.verbandName === 'DPV') {
        return 'dpv-blue';
      }
      return 'bdp-yellow';
    },
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0}`;
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
    getDateFormat(value) {
      return moment(value).format('DD.MM.YYYY');
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
