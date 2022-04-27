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
        show-expand
        single-expand
        hide-default-footer
        item-key="createdAt"
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
          <template v-slot:expanded-item="{ item }">
          <template v-for="(string, index) in getBody(filterNulls(item))" >
            <v-list-item :key="index">
              <v-list-item-content>
                <v-list-item-title>{{ string }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
            <v-list-item>
            <v-list-item-content>
              <b>Verantwortlich: </b>
              <template v-for="(string) in item.responsiblePersons">
                {{ `${string}, `}}
              </template>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
            <v-list-item-content>
              <b>Buchungsoption: </b>
              <p v-for="(item, i) in item.bookingOptions" :key="i">
                {{ item.bookingOptions }}: {{ item.sum}}
              </p>
              </v-list-item-content>
            </v-list-item>
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
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment'; // eslint-disable-line

export default {
  mixins: [serviceMixin],
  data: () => ({
    data: [],
    expanded: [],
    filter: {
      justConfirmed: true,
    },
    headers: [
      { text: 'Bestätigt', value: 'isConfirmed' },
      { text: 'Datum', value: 'createdAt' },
      { text: 'Bund', value: 'scoutOrganisation.bund' },
      { text: 'Name', value: 'scoutOrganisation.name' },
      { text: 'Teilnehmende', value: 'participantCount' },
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
      const participantCount = this.getItems.reduce(
        (accum, item) => accum + item.participantCount,
        0,
      ); // eslint-disable-line
      return `${participantCount || 0} Personen`;
    },
    getTotalStamm() {
      const numberStammBdp = this.getItems.length;
      return `Stämme ${numberStammBdp || 0}`;
    },
  },

  methods: {
    filterNulls(items) {
      return items.tags.filter((i) => !!this.getValueField(i));
    },
    getBody(item) {
      return item.map((t) => `${t.name}: ${this.getValueField(t)}`);
    },
    getValueField(item) {
      let value = '';
      if (item.booleanField) {
        value = item.booleanField;
      }
      if (item.integerField) {
        value = item.integerField;
      }
      if (item.timeField) {
        value = item.timeField;
      }
      if (item.stringField) {
        value = item.stringField;
      }
      switch (value) {
        case true:
          return 'Ja';
        case false:
          return 'Nein';
        default:
          return value;
      }
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
