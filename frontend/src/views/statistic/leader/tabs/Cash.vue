<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0">
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="12">
                <v-checkbox
                  v-model="filter.justConfirmed"
                  label="Nur Bestätigt"
                  hide-details/>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table :headers="headers"
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
          </v-icon>
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ formatDate(item.createdAt) }}
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
          <td :colspan="headers.length">
            <v-list-item>
              <v-list-item-content>
                <v-data-table
                  :headers="headersBookingOptions"
                  :items="getItemsBookingOptions(item)"
                  :items-per-page="itemsPerPage"
                  hide-default-footer
                  item-key="createdAt">
                  <template v-slot:top>
                    <v-toolbar flat>
                      <v-toolbar-title>Gebuchte Optionen</v-toolbar-title>
                      <v-spacer/>
                    </v-toolbar>
                  </template>
                </v-data-table>
              </v-list-item-content>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-data-table
                  :headers="headersCash"
                  :items="getItemsCash(item)"
                  :items-per-page="itemsPerPage"
                  hide-default-footer
                  item-key="createdAt"
                  no-data-text="Keine Buchung vorhanden">
                  <template v-slot:top>
                    <v-toolbar flat>
                      <v-toolbar-title>Überweisungen</v-toolbar-title>
                      <v-spacer/>
                      <v-spacer/>
                      <v-dialog v-model="dialog" max-width="500px">
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            @click="onNewClicked(item)"
                            color="primary"
                            dark
                            class="mb-2"
                            v-bind="attrs"
                            v-on="on">
                            Neue Überweisung
                          </v-btn>
                        </template>
                      </v-dialog>
                    </v-toolbar>
                  </template>
                  <template v-slot:[`item.transferDate`]="{ item }">
                    {{ formatDate(item.transferDate) }}
                  </template>
                  <template v-slot:[`item.amount`]="{ item }">
                    {{ getPrice(item.amount) }}
                  </template>
                  <template v-slot:[`item.actions`]="{ item }">
                    <v-icon
                      small
                      class="mr-2"
                      @click="onEditClicked(item)">
                      mdi-pencil
                    </v-icon>
                    <v-icon
                      small
                      @click="onDeleteClicked(item)">
                      mdi-delete
                    </v-icon>
                  </template>
                </v-data-table>
              </v-list-item-content>
            </v-list-item>
          </td>
        </template>
        <template slot="body.append">
          <tr>
            <th colspan="3">Summe</th>
            <th>{{ getTotalStamm }}</th>
            <th>{{ getTotalPrice }}</th>
            <th>{{ getTotalPaid }}</th>
            <th>{{ getTotalOpen }}</th>
          </tr>
        </template>
      </v-data-table>
    </v-row>
    <TranserCreationModal
      ref="preEventCreationRef"
      @createTransfer="createTransfer"
      @editTransfer="editTransfer"/>
    <TransferDeleteModal
      ref="transferDeleteModalRef"
      @refresh="onRefresh"/>
  </v-container>
</template>

<script>
import TranserCreationModal from '@/components/dialog/TranfserCreationModal.vue';
import TransferDeleteModal from '@/components/dialog/TransferDeleteModal.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment'; // eslint-disable-line
import axios from 'axios';

export default {
  mixins: [apiCallsMixin],
  components: {
    TranserCreationModal,
    TransferDeleteModal,
  },
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
        text: 'Betreff',
        value: 'transferSubject',
      },
      {
        text: 'Datum',
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
      {
        text: 'Aktionen',
        value: 'actions',
        sortable: false,
      },
    ],
    dialog: false,
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
    formatDate(item) {
      return moment(item)
        .format('DD.MM.YYYY');
    },
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
    onRefresh() {
      this.getData(this.eventId);
    },
    onEditClicked(data) {
      this.$refs.preEventCreationRef.openEdit(data);
    },
    onNewClicked(item) {
      this.$refs.preEventCreationRef.open(item.id);
    },
    onDeleteClicked(data) { //eslint-disable-line
      this.$refs.transferDeleteModalRef.open(data);
    },
    createTransfer(data, registrationId) {
      axios
        .post(`${this.API_URL}/event/cash/income/`, {
          amount: data.amount,
          transferSubject: data.transferSubject,
          transferDate: data.transferDate,
          transferPerson: data.transferPerson,
          transferReferenceId: data.transferReferenceId,
          description: data.description,
          registration: registrationId,
        })
        .then(() => {
          this.onRefresh();
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim erstellen des Überweisungseintrags aufgetreten,'
              + ' bitte probiere es später nocheinmal.',
            color: 'error',
            timer: 5000,
          });
        });
    },
    editTransfer(data, registrationId) {
      axios
        .patch(`${this.API_URL}/event/cash/income/${data.id}/`, {
          amount: data.amount,
          transferSubject: data.transferSubject,
          transferDate: data.transferDate,
          transferPerson: data.transferPerson,
          transferReferenceId: data.transferReferenceId,
          description: data.description,
          registration: registrationId,
        })
        .then(() => {
          this.onRefresh();
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim erstellen des Überweisungseintrags aufgetreten,'
              + ' bitte probiere es später nocheinmal.',
            color: 'error',
            timer: 5000,
          });
        });
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
