<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <v-autocomplete
                  :loading="loading"
                  :items="stammList"
                  v-model="filter.stamm"
                  label="Stamm"
                  item-text="scoutOrganisation.name"
                ></v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
        v-if="filter.stamm"
        :headers="headers"
        :items="getPersons"
        :items-per-page="itemsPerPage"
        :expanded.sync="expanded"
        show-expand
        single-expand
        hide-default-footer
        item-key="createdAt">
        <template v-slot:[`item.isConfirmed`]="{ item }">
          <v-icon :color="item.isConfirmed ? 'green' : 'red'">
            {{
              item.isConfirmed ? 'mdi-check-circle' : 'mdi-close-circle'
            }}</v-icon
          >
        </template>
        <template v-slot:[`item.birthday`]="{ item }">
          {{ moment(item.birthday).format('DD.MM.YYYY') }}
        </template>
        <template v-slot:expanded-item="{ item }">
          <v-list-item
            v-if=" item.street && item.zipCode">
            <v-list-item-content>
              <b>Adresse: </b>
              <template>
                {{ `${item.street} ${item.zipCode.zipCode} ${item.zipCode.city} ` }}
                {{ `Tel: ${item.phoneNumber}` }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="item.street">
            <v-list-item-content>
              <b>Essen: </b>
              <template v-for="habit in item.eatHabit">
                {{ `${habit}, ` }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="item.leader">
            <v-list-item-content>
              <b>Amt: </b>
              {{ item.leader }}
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="item.gender">
            <v-list-item-content>
              <b>Geschlecht: </b>
              {{ item.gender }}
            </v-list-item-content>
          </v-list-item>
          <v-list-item
            v-if="item.bookingOption">
            <v-list-item-content>
              <b>Option: </b>
              {{ item.bookingOption.name }}
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-data-table>
    </v-row>
    <v-row v-if="!loading && !filter.stamm" justify="center">
    <p> Bitte wähle einen Stamm</p>
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
    loading: true,
    filter: {
      stamm: null,
    },
    headers: [
      { text: 'Vorname', value: 'firstName' },
      { text: 'Fahrtenname', value: 'scoutName' },
      { text: 'Nachname', value: 'lastName' },
      { text: 'Geburtsdatum', value: 'birthday' },
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
    stammList() {
      return this.data;
    },
    getItems() {
      const data = this.data.filter(
        (item) => item.scoutOrganisation.name === this.filter.stamm,
      );
      return data;
    },
    getPersons() {
      const data = this.data.filter(
        (item) => item.scoutOrganisation.name === this.filter.stamm,
      );
      const personArray = [];
      const personsObj = (data && data.length > 0 && data) || [];

      personsObj.forEach((person) => {
        person.registrationparticipantSet.forEach((item) => {
          personArray.push(item);
        });
      });
      return personArray;
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
      this.loading = true;
      this.getRegistrationSummaryDetails(eventId).then((responseObj) => {
        this.data = responseObj.data[0].registrationSet;
        this.loading = false;
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
