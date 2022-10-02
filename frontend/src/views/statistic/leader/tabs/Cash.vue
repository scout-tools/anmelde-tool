<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0">
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="6">
                <v-checkbox
                    v-model="filter.justConfirmed"
                    label="Nur Bestätigt"
                    hide-details/>
              </v-col>
              <v-col cols="6">
                <v-btn
                    v-if="isTeam"
                    class="ma-2"
                    @click="openReminderDialog">
                  <v-icon color="#008000" left> mdi-email-arrow-right</v-icon>
                  Erinnerungsmail
                </v-btn>
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
        <template v-slot:[`item.mailButton`]="{ item }">
          <v-btn
            color="success"
            dark
            icon
            @click="onNewClicked(item)">
            <v-icon>
              mdi-cash-100
            </v-icon>
          </v-btn>
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
              <v-list-item-title class="justify-center text-center">
                Referenz Id: <span><strong> {{ item.refId }} </strong></span>
              </v-list-item-title>
            </v-list-item>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  Verantwortliche Personen(en)
                </v-list-item-title>
                <v-list dense flat>
                  <v-list-item dense
                               v-for="(pers, i) in item.responsiblePersons"
                               :key="i">
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ i+1 }}. Person:
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        Fahrten Name: {{ pers.userextended.scoutName }}
                      </v-list-item-subtitle>
                      <v-list-item-subtitle>
                        Name: {{ pers.firstName }} {{ pers.lastName }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-list-item-content>
            </v-list-item>
            <v-btn
                @click="onNewClicked(item)"
                color="success"
                class="mb-2">
              <v-icon>mdi-plus</v-icon>
              Buchung hinzufügen
            </v-btn>
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
                      <v-toolbar-title>Buchungen</v-toolbar-title>
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
                        @click="onNewClicked(item)">
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
                      <v-toolbar-title>Kostenpunkte</v-toolbar-title>
                      <v-spacer/>
                    </v-toolbar>
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
        ref="transerCreationModalRef"
        @createTransfer="createTransfer"
        @editTransfer="editTransfer"/>
    <TransferDeleteModal
        ref="transferDeleteModalRef"
        @refresh="onRefresh"/>
    <SendPaymentReminderModal
        ref="sendPaymentReminderModalRef"/>
  </v-container>
</template>

<script>
import TranserCreationModal from '@/components/dialog/TranfserCreationModal.vue';
import TransferDeleteModal from '@/components/dialog/TransferDeleteModal.vue';
import SendPaymentReminderModal from '@/components/dialog/SendPaymentReminderModal.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment'; // eslint-disable-line
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  mixins: [apiCallsMixin],
  components: {
    TranserCreationModal,
    TransferDeleteModal,
    SendPaymentReminderModal,
  },
  data: () => ({
    data: [],
    expanded: [],
    filter: {
      justConfirmed: true,
    },
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
    eventData: null,
  }),
  computed: {
    ...mapGetters(['userinfo']),
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
      return `${this.financial(price) || 0} €`;
    },
    getTotalPaid() {
      const price = this.getItems.reduce((accum, item) => accum + item.payement.paid, 0);
      return `${this.financial(price) || 0} €`;
    },
    getTotalOpen() {
      const price = this.getItems.reduce((accum, item) => accum + item.payement.open, 0);
      return `${this.financial(price) || 0} €`;
    },
    getTotalStamm() {
      const numberStamm = this.getItems.length;
      return `Stämme ${numberStamm || 0}`;
    },
    isTeam() {
      if (this.userinfo && this.userinfo.roles && this.userinfo.roles.length > 0) {
        return this.userinfo.roles.includes('anmelde_tool_team');
      }
      return 0;
    },
    headers() {
      const heads = [
        {
          text: '',
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
          value: 'mailButton',
        },
        {
          text: '',
          value: 'data-table-expand',
        },
      ];

      if (this.eventData
          && (this.eventData.singleRegistrationLevel.id === 6
              || this.eventData.groupRegistrationLevel.id === 6)) {
        heads.splice(
          3,
          0,
          {
            text: 'Stamm',
            value: 'scoutOrganisation.stamm',
          },
        );
      }

      return heads;
    },
  },
  methods: {
    financial(x) {
      return Number.parseFloat(x)
        .toFixed(2);
    },
    formatDate(item) {
      return moment(item)
        .format('DD.MM.YYYY');
    },
    getBody(item) {
      return item;
    },
    getPrice(item) {
      return this.financial(item) ? `${this.financial(item)} €` : '0.00 €';
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
      Promise.all([
        this.getCashSummary(eventId),
        this.getEventOverviewById(eventId),
      ])
        .then((responseObj) => {
            this.data = responseObj[0].data[0]; // eslint-disable-line
            this.eventData = responseObj[1].data; // eslint-disable-line
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
      this.$refs.transerCreationModalRef.openEdit(data);
    },
    onNewClicked(data) {
      this.$refs.transerCreationModalRef.open(data, data.id);
    },
    openReminderDialog() {
      this.$refs.sendPaymentReminderModalRef.open(this.eventId);
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
