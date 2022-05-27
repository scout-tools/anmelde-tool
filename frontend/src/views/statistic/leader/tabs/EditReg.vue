<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="6">
                <v-checkbox
                  v-model="filter.justConfirmed"
                  label="Nur Bestätigt"
                  hide-details
                />
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
        :items="getItems"
        :items-per-page="itemsPerPage"
        hide-default-footer
        item-key="createdAt"
      >
        <template v-slot:[`item.isConfirmed`]="{ item }">
          <v-icon :color="item.isConfirmed ? 'green' : 'red'">
            {{ item.isConfirmed ? 'mdi-check-circle' : 'mdi-close-circle' }}
          </v-icon>
        </template>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ moment(item.createdAt).format('DD.MM.YYYY') }}
        </template>
        <template v-slot:[`item.numberParticipant`]="{ item }">
          <td v-html="getNumberParticipant(item)" disabled></td>
        </template>
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon color="primary" class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon color="error" @click="deleteItem(item)"> mdi-delete </v-icon>
        </template>
      </v-data-table>
    </v-row>
    <confirm-registration-edit-modal ref="confirmRegistrationEditModal" />
    <DeleteModal ref="deleteModal" />
  </v-container>
</template>

<script>
import serviceMixin from '@/mixins/serviceMixin';
import BookingFilter from '@/components/common/BookingFilter.vue';
import ConfirmRegistrationEditModal from '@/views/registration/components/PreForm.vue';
import DeleteModal from '@/views/registration/components/DeleteModal.vue';

export default {
  mixins: [serviceMixin],
  components: {
    BookingFilter,
    ConfirmRegistrationEditModal,
    DeleteModal,
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
        text: 'Teilnehmende',
        value: 'participantCount',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
      { text: 'Aktionen', value: 'actions', sortable: false },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
    loading: false,
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
    editItem(item) {
      console.log(item);
      this.editRegistration(item);
    },
    deleteItem(item) {
      this.deleteRegistration(item);
    },
    editRegistration(item) {
      this.$refs.confirmRegistrationEditModal.show(item.id);
    },
    deleteRegistration(item) {
      this.$refs.deleteModal.show(item.id);
    },
    getRegisteredId(item, single = false) {
      if (!item.registrationOptions) {
        return null;
      }
      if (item.registrationOptions.groupId && !single) {
        return item.registrationOptions.groupId;
      }
      if (item.registrationOptions.singleId) {
        return item.registrationOptions.singleId;
      }
      return null;
    },
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
    getData(eventId, param) {
      this.loading = true;

      Promise.all([
        this.getRegistrationSummary(eventId, param),
        this.getBookingOptions(eventId),
      ])
        .then((values) => {
          this.data = values[0].data[0].registrationSet; //eslint-disable-line
          this.bookingOptionList = values[1].data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
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
