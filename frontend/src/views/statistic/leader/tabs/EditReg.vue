<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center pa-0">
              <RegistrationFilter
                  :eventId="eventId"
                  @onFilterSelected="onFilterSelected"/>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto mb-3">
      <v-card flat class="pa-3">
        <v-data-table
            :loading="loading"
            :headers="headers"
            :items="data"
            single-expand
            item-key="createdAt"
            :options.sync="options"
            :server-items-length="totalCount"
            :items-per-page="itemsPerPage"
            must-sort
            sort-by="createdAt"
            :footer-props="{itemsPerPageText: 'Anmeldungen pro Seite'}"
            no-data-text="Keine Anmeldungen Gefunden."
            loading-text="Lade Anmeldungen...">
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
          <template v-slot:[`footer.page-text`]="items">
            {{ items.pageStart }} - {{ items.pageStop }} von {{ items.itemsLength }} Anmeldungen
          </template>
        </v-data-table>
      </v-card>
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
    loading: false,
    totalCount: 0,
    registrationFilterParams: null,
    paginationParams: null,
    options: {},
    itemsPerPage: 10,
    expanded: [],
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
    getData() {
      this.loading = true;

      const combined = new URLSearchParams();
      // eslint-disable-next-line no-restricted-syntax
      for (const [key, val] of this.registrationFilterParams.entries()) {
        combined.append(key, val);
      }
      // eslint-disable-next-line no-restricted-syntax
      for (const [key, val] of this.paginationParams.entries()) {
        combined.append(key, val);
      }

      this.getEventSummary(this.eventId, combined)
        .then((result) => {
          this.data = result.data.results; //eslint-disable-line
          this.totalCount = result.data.count;
        })
        .catch((error) => {
          const msg = error.response.data.detail ? error.response.data.detail : error.response.data;
          this.$root.globalSnackbar.show({
            message: msg,
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(param) {
      this.registrationFilterParams = param;
      this.paginationParams.set('page', 1);
      this.getData();
    },
  },
  created() {
    this.paginationParams = new URLSearchParams();
    this.paginationParams.append('page-size', this.itemsPerPage);
    this.paginationParams.append('page', '1');
    this.paginationParams.append('ordering', 'created_at');
    this.registrationFilterParams = new URLSearchParams();
    this.registrationFilterParams.append('confirmed', 'true');
    this.getData();
  },
  watch: {
    options: {
      handler() {
        const {
          sortBy,
          sortDesc,
          page,
          itemsPerPage,
        } = this.options;

        const pageParams = new URLSearchParams();
        pageParams.append('page-size', itemsPerPage);
        pageParams.append('page', page);

        if (sortBy) {
          pageParams.append('ordering', sortBy);
        } else {
          pageParams.append('ordering', 'lastName');
        }
        pageParams.append('order-desc', sortDesc);

        this.paginationParams = pageParams;
        this.getData();
      },
      deep: true,
    },
  },
};
</script>
