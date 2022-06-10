<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <RegistrationFilter
                  :bookingOptionList="bookingOptionList"
                  :loading="loading"
                  @onFilterSelected="onFilterSelected"/>
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
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon small color="primary" class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
          <v-icon small color="error" @click="deleteItem(item)"> mdi-delete</v-icon>
          <v-icon small color="secondary" @click="onAddResponsablePerson(item)">
            mdi-share-variant
          </v-icon>
        </template>
      </v-data-table>
    </v-row>
    <confirm-registration-edit-modal ref="confirmRegistrationEditModal"/>
    <DeleteModal ref="deleteModal"/>
    <DialogAddResponsablePerson ref="dialogAddResponsablePerson"/>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';
import ConfirmRegistrationEditModal from '@/views/registration/components/PreForm.vue';
import DeleteModal from '@/views/registration/components/DeleteModal.vue';
import DialogAddResponsablePerson from '@/components/dialog/DialogAddResponsablePerson.vue';
import moment from 'moment';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
    ConfirmRegistrationEditModal,
    DeleteModal,
    DialogAddResponsablePerson,
  },
  data: () => ({
    data: [],
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
        text: 'Aktionen',
        value: 'actions',
        sortable: false,
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 100,
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
    getTotalRegistrations() {
      return this.data.length;
    },
    getTotalPariticipants() {
      return this.data.map((x) => x.participantCount)
        .reduce((pv, cv) => pv + cv, 0);
    },
  },
  methods: {
    formatDate(item) {
      return moment(item)
        .locale('de')
        .format('l');
    },
    onAddResponsablePerson(item) {
      this.$refs.dialogAddResponsablePerson.open(item);
    },
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
    getResponsiblePersonsersons(item) {
      return item.responsiblePersons.join(', ');
    },
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0}`;
    },
    getData(param) {
      this.loading = true;

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
    onFilterSelected(params) {
      this.getData(params);
    },
  },
  created() {
    this.getData(null);
  },
};
</script>
