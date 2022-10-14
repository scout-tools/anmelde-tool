<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <RegistrationFilter
                :eventId="eventId"
                @onFilterSelected="onFilterSelected"
                preSelectStamm="true"/>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row v-if="data" justify="center" class="overflow-y: auto">
      <v-data-table
          :loading="loading"
          :items="getPersonsList"
          must-sort
          :expanded.sync="expanded"
          :headers="headers"
          :footer-props="{
            itemsPerPageText: 'Personen pro Seite',
            'items-per-page-options': [10, 20, 30, 40, 50, -1]
          }"
          show-expand
          single-expand
          :options.sync="options"
          :server-items-length="totalCount"
          :items-per-page="itemsPerPage"
          sort-by="lastName"
          item-key="createdAt"
          no-data-text="Keine Teilnehmer Gefunden."
          loading-text="Lade Teilnehmer...">
        <template v-slot:[`item.birthday`]="{ item }">
          {{
            getBirthday(item)
          }}
        </template>
        <template v-slot:expanded-item="{ item }">
          <v-list-item v-if="item.street && item.zipCode">
            <v-list-item-content>
              <b>Adresse: </b>
              <template>
                {{ `${item.street}, ${item.zipCode.zipCode} ${item.zipCode.city}` }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.phoneNumber">
            <v-list-item-content>
              <b>Tel:</b>
              <template>
                {{ item.phoneNumber }}
              </template>
            </v-list-item-content>
          </v-list-item>
          <v-list-item v-if="item.eatHabit">
            <v-list-item-content>
              <b>Essen: </b>
              {{ getEatHabits(item.eatHabit) }}
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
        <template v-slot:[`footer.page-text`]="items">
          {{ items.pageStart }} - {{ items.pageStop }} von {{ items.itemsLength }} Personen
        </template>
      </v-data-table>
    </v-row>
    <v-row v-else justify="center">
      <p>Bitte wähle einen Stamm</p>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';
import moment from 'moment';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
  },
  data: () => ({
    data: [],
    expanded: [],
    loading: true,
    headers: [
      {
        text: 'Vorname',
        value: 'firstName',
      },
      {
        text: 'Fahrtenname',
        value: 'scoutName',
      },
      {
        text: 'Nachname',
        value: 'lastName',
      },
      {
        text: 'Alter',
        value: 'birthday',
      },
      {
        text: 'Stamm',
        value: 'scoutOrganisation',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 5,
    options: {},
    totalCount: 0,
    registrationFilterParams: null,
    paginationParams: null,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getPersonsList() {
      if (this.data) {
        return this.data;
      }
      return [];
    },
  },
  methods: {
    onFilterSelected(param) {
      this.registrationFilterParams = param;
      this.paginationParams.set('page', 1);
      this.getData();
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

      this.getRegistrationSummaryDetails(this.eventId, combined)
        .then((result) => {
            this.data = result.data.results; //eslint-disable-line
          this.totalCount = result.data.count;
        })
        .catch((err) => {
          this.$root.globalSnackbar.show({
            message: err.data,
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getBirthday(item) {
      if (item.birthday) {
        return moment()
          .diff(item.birthday, 'years');
      }
      return '/';
    },
    getEatHabits(items) {
      if (items) {
        return items.join(', ');
      }
      return '/';
    },
  },
  created() {
    this.paginationParams = new URLSearchParams();
    this.paginationParams.append('page-size', this.itemsPerPage);
    this.paginationParams.append('page', '1');
    this.paginationParams.append('ordering', 'last_name');
    this.registrationFilterParams = new URLSearchParams();
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
