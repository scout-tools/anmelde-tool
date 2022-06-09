<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="6">
                <v-checkbox
                    v-model="justConfirmed"
                    label="Nur Bestätigt"
                    @change="getData"
                    hide-details/>
              </v-col>
              <v-col cols="6">
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
      <v-data-table
          :headers="headers"
          :items="data"
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
            }}
          </v-icon>
        </template>
        <template v-slot:[`item.single`]="{ item }">
          <v-icon :color="item.single ? 'green' : 'red'">
            {{
              item.single ? 'mdi-check-circle' : 'mdi-close-circle'
            }}
          </v-icon>
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{
            formatDate(item.createdAt)
          }}
        </template>
        <template v-slot:[`item.updatedAt`]="{ item }">
          {{
            formatDate(item.updatedAt)
          }}
        </template>
        <template v-slot:[`item.numberParticipant`]="{ item }">
          <td v-html="getNumberParticipant(item)" disabled></td>
        </template>
        <template v-slot:expanded-item="{ item }">
          <td :colspan="headers.length">
            <v-list-item>
              <v-list-item-content>
                <b>Verantwortlich(e): </b>
                {{ getResponsiblePersonsersons(item) }}
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <b>Buchungsoption: </b>
                <p v-for="(item, i) in item.bookingOptions" :key="i">
                  {{ item.bookingOptions }}: {{ item.sum }}
                </p>
              </v-list-item-content>
            </v-list-item>
          </td>
        </template>
        <template slot="body.append">
          <tr>
            <th colspan="4">Summe</th>
            <th colspan="2">Registrierungen: {{ getTotalRegistrations }}</th>
            <th colspan="2"> Teilnehmer: {{ getTotalPariticipants }}</th>
          </tr>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>
import moment from 'moment';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BookingFilter from '@/components/common/BookingFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    BookingFilter,
  },
  data: () => ({
    data: [],
    expanded: [],
    justConfirmed: true,
    selectedBookingOption: null,
    headers: [
      {
        text: 'Bestätigt',
        value: 'isConfirmed',
      },
      {
        text: 'Einzel Anmeldung',
        value: 'single',
      },
      {
        text: 'Erstellt',
        value: 'createdAt',
      },
      {
        text: 'Zuletzt Bearbeitet',
        value: 'updatedAt',
      },
      {
        text: 'Bund',
        value: 'scoutOrganisation.bund',
      },
      {
        text: 'Name',
        value: 'scoutOrganisation.name',
      },
      {
        text: 'Teilnehmende',
        value: 'participantCount',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
    loading: false,
    bookingOptionList: [],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    getTotalRegistrations() {
      return this.data.length;
    },
    getTotalPariticipants() {
      return this.data.map((x) => x.participantCount).reduce((pv, cv) => pv + cv, 0);
    },
  },
  methods: {
    getResponsiblePersonsersons(item) {
      return item.responsiblePersons.join(', ');
    },
    formatDate(item) {
      return moment(item)
        .locale('de')
        .format('l');
    },
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0}`;
    },
    getData() {
      this.loading = true;
      const param = new URLSearchParams();
      param.append('confirmed', this.justConfirmed);
      if (this.selectedBookingOption) {
        this.selectedBookingOption.forEach((value) => {
          param.append('booking-option', value);
        });
      }

      Promise.all([
        this.getEventSummary(this.eventId, param),
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
    onFilterSelected(value) {
      this.selectedBookingOption = value;
      this.getData();
    },
  },
  created() {
    this.getData();
  },
};
</script>
