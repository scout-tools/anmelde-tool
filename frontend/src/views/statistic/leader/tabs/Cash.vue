<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
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
        :loading="loading">
        <template v-slot:[`item.isConfirmed`]="{ item }">
          <v-icon :color="item.isConfirmed ? 'green' : 'red'">
            {{
              item.isConfirmed ? 'mdi-check-circle' : 'mdi-close-circle'
            }}
          </v-icon
          >
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{
            moment(item.createdAt)
              .format('DD.MM.YYYY')
          }}
        </template>
        <template v-slot:[`item.numberParticipant`]="{ item }">
          <td v-html="getNumberParticipant(item)" disabled></td>
        </template>
        <template v-slot:[`item.payement.price`]="{ item }">
          <td v-html="getPrice(item.payement.price)"/>
        </template>
        <template v-slot:[`item.payement.paid`]="{ item }">
          <td v-html="getPrice(item.payement.paid)"/>
        </template>
        <template v-slot:[`item.payement.open`]="{ item }">
          <td :class="item.payement.open > 0 ? 'open-position' : 'closed-position'"
              v-html="getPrice(item.payement.open)"/>
        </template>
        <template v-slot:expanded-item="{ item }">
          <!--          <td :colspan="headers.length">-->
          <!--            <pre>{{ getBody(item) }}</pre>-->
          <!--          </td>-->
          <td class="px-2 py-2" :colspan="headers.length">
            Einzelheiten:
            <v-data-table
              :headers="headersBookingOptions"
              :items="getItemsBookingOptions(item)"
              :items-per-page="itemsPerPage"
              hide-default-footer
              item-key="createdAt">
            </v-data-table>
            Überweisungen:
            <v-data-table
              :headers="headersCash"
              :items="getItemsCash(item)"
              :items-per-page="itemsPerPage"
              hide-default-footer
              item-key="createdAt">
              <template v-slot:[`item.amount`]="{ item }">
          <td v-html="getPrice(item.amount)"/>
        </template>
        <template v-slot:[`item.transferDate`]="{ item }">
          {{
            moment(item.transferDate)
              .format('DD.MM.YYYY')
          }}
        </template>
      </v-data-table>
      </td>
</template>
<template slot="body.append">
  <tr>
    <th>Summe</th>
    <th colspan="3">{{ getTotalStamm }}</th>
    <th>{{ getTotalPrice }}</th>
    <th>{{ getTotalPaid }}</th>
    <th>{{ getTotalOpen }}</th>
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
      {
        text: 'Bestätigt',
        value: 'isConfirmed',
      },
      {
        text: 'Datum',
        value: 'createdAt',
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
        text: 'Gesamtpreis',
        value: 'payement.price',
      },
      {
        text: 'Bezahlt',
        value: 'payement.paid',
      },
      {
        text: 'Offen',
        value: 'payement.open',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    headersBookingOptions: [
      {
        text: 'Buchoption',
        value: 'bookingOptions',
      },
      {
        text: 'Anzahl',
        value: 'sum',
      },
      {
        text: 'Preis',
        value: 'price',
      },
    ],
    headersCash: [
      {
        text: 'Überweisungsbetreff',
        value: 'transferSubject',
      },
      {
        text: 'Überweisungsdatum',
        value: 'transferDate',
      },
      {
        text: 'Referenz Id',
        value: 'transferReferenceId',
      },
      {
        text: 'Person',
        value: 'transferPerson',
      },
      {
        text: 'Betrag',
        value: 'amount',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
    loading: false,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getItems() {
      if (!this.data || !this.data.registrationSet) return [];
      const data = this.data.registrationSet.filter(
        (item) => item.isConfirmed === this.filter.justConfirmed || !this.filter.justConfirmed,
      );
      return data;
    },
    getTotalPrice() {
      const price = this.getItems.reduce((accum, item) => accum + item.payement.price, 0);
      return `${price || 0} €`;
    },
    getTotalPaid() {
      const price = this.getItems.reduce((accum, item) => accum + item.payement.paid, 0);
      return `${price || 0} €`;
    },
    getTotalOpen() {
      const price = this.getItems.reduce((accum, item) => accum + item.payement.open, 0);
      return `${price || 0} €`;
    },
    getTotalStamm() {
      const numberStamm = this.getItems.length;
      return `Stämme ${numberStamm || 0}`;
    },
  },
  methods: {
    getBody(item) {
      return item;
    },
    getPrice(item) {
      return item ? `${item} €` : '0 €';
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
      this.getCashSummary(eventId)
        .then((responseObj) => {
          this.data = responseObj.data[0]; // eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getItemsBookingOptions(item) {
      return item.bookingOptions;
    },
    getItemsCash(item) {
      return item.cashincomeSet;
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>

<style scoped>
.dpv-blue {
  background-color: rgba(56, 117, 238, 0.082);
}

.bdp-yellow {
  background-color: #ffcc0227;
}

.open-position {
  color: red;
}

.closed-position {
  color: green;
}
</style>
