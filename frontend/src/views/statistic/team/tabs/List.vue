<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <RegistrationFilter
                :eventId="eventId"
                @onFilterSelected="onFilterSelected"/>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-card flat>
        <v-data-table
            :loading="loading"
            :headers="headers"
            :items="data"
            :expanded.sync="expanded"
            show-expand
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
<!--          <template v-slot:[`group.header`]="{group, isOpen, toggle, remove}">-->
<!--            <td :colspan="headers.length">-->
<!--              <v-icon @click="toggle">-->
<!--                {{ isOpen ? 'mdi-minus' : 'mdi-plus' }}-->
<!--              </v-icon>-->
<!--              <span>-->
<!--                <strong>{{ getGroupName(group) }}</strong>-->
<!--              </span>-->
<!--              <v-icon @click="remove">-->
<!--                mdi-close-->
<!--              </v-icon>-->
<!--            </td>-->
<!--          </template>-->
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
          <template v-slot:[`body.append`]>
            <tr>
              <th colspan="4">Summe</th>
              <th colspan="2">Registrierungen: {{ getTotalRegistrations }}</th>
              <th colspan="2"> Teilnehmer: {{ getTotalPariticipants }}</th>
            </tr>
          </template>
          <template v-slot:[`footer.page-text`]="items">
            {{ items.pageStart }} - {{ items.pageStop }} von {{ items.itemsLength }} Anmeldungen
          </template>
        </v-data-table>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import moment from 'moment';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
  },
  data: () => ({
    data: [],
    expanded: [],
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
        text: 'Stamm',
        value: 'scoutOrganisation.name',
      },
      {
        text: 'Teilnehmende',
        value: 'participantCount',
        sortable: false,
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    loading: false,
    totalCount: 0,
    registrationFilterParams: null,
    paginationParams: null,
    options: {},
    itemsPerPage: 10,
  }),
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
      this.paginationParams.set('page', 1);
      this.registrationFilterParams = param;
      this.getData();
    },
    getGroupName(name) {
      if (name) {
        return name;
      }
      return 'DPV';
    },
  },
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
