<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="pa-0" flat>
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
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <v-autocomplete
                  :loading="loading"
                  :items="stammList"
                  v-model="filter.stamm"
                  label="Stamm"
                  item-text="registration.scoutOrganisation.name"
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
        item-key="createdAt"
      >
        <template v-slot:[`item.isConfirmed`]="{ item }">
          <v-icon :color="item.isConfirmed ? 'green' : 'red'">
            {{
              item.isConfirmed ? 'mdi-check-circle' : 'mdi-close-circle'
            }}</v-icon
          >
        </template>
        <template v-slot:[`item.birthday`]="{ item }">
          {{
            `${moment().diff(
              item.birthday,
              'years',
            )}`
          }}
        </template>
        <template v-slot:expanded-item="{ item }">
          <v-list-item v-if="item.street && item.zipCode">
            <v-list-item-content>
              <b>Adresse: </b>
              <template>
                {{
                  `${item.street} ${item.zipCode.zipCode} ${item.zipCode.city} `
                }}
                {{ `Tel: ${item.phoneNumber}` }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.street">
            <v-list-item-content>
              <b>Essen: </b>
              <template v-for="habit in item.eatHabit">
                {{ `${habit}, ` }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.leader">
            <v-list-item-content>
              <b>Amt: </b>
              {{ item.leader }}
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.gender">
            <v-list-item-content>
              <b>Geschlecht: </b>
              {{ item.gender }}
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.bookingOption">
            <v-list-item-content>
              <b>Option: </b>
              {{ item.bookingOption.name }}
            </v-list-item-content>
          </v-list-item>
        </template>
      </v-data-table>
    </v-row>
    <v-row v-if="!loading && !filter.stamm" justify="center">
      <p>Bitte wähle einen Stamm</p>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment'; // eslint-disable-line
import BookingFilter from '@/components/common/BookingFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    BookingFilter,
  },
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
      { text: 'Alter', value: 'birthday' },
      { text: '', value: 'data-table-expand' },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
    bookingOptionList: [],
    selectedBookingOption: null,
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
      const personArray = this.data.filter(
        (item) => item.registration.scoutOrganisation.name === this.filter.stamm,
      );
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
    onFilterSelected(values) {
      const params = new URLSearchParams();
      if (values) {
        values.forEach((value) => {
          params.append('booking-option', value);
        });
      }
      this.getData(this.eventId, params);
    },
    getData(eventId, param) {
      this.loading = true;

      Promise.all([
        this.getRegistrationSummaryDetails(eventId, param),
        this.getBookingOptions(eventId),
      ])
        .then((values) => {
          this.data = values[0].data; //eslint-disable-line
          console.log(this.data);
          this.bookingOptionList = values[1].data; //eslint-disable-line
        })
        .finally(() => {
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
