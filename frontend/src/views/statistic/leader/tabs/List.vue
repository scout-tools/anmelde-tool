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
          :items="getPersons"
          must-sort
          :expanded.sync="expanded"
          :headers="headers"
          :footer-props="{itemsPerPageText: 'Personen pro Seite'}"
          show-expand
          single-expand
          sort-by="lastName"
          item-key="createdAt"
          no-data-text="Keine Anmeldungen Gefunden."
          loading-text="Lade Anmeldungen...">
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
        text: '',
        value: 'data-table-expand',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 25,
    options: {},
    totalCount: 0,
    registrationFilterParams: null,
    paginationParams: null,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getPersons() {
      const result = [];
      this.data.map((x) => x.participants)
        .forEach((item) => {
          item.forEach((person) => {
            result.push(person);
          });
        });
      return result;
    },
  },
  methods: {
    onFilterSelected(param) {
      this.registrationFilterParams = param;
      this.getData();
    },
    getData() {
      this.loading = true;

      const combined = new URLSearchParams();
      // eslint-disable-next-line no-restricted-syntax
      for (const [key, val] of this.registrationFilterParams.entries()) {
        combined.append(key, val);
      }
      //
      // eslint-disable-next-line no-restricted-syntax
      // for (const [key, val] of this.paginationParams.entries()) {
      //   combined.append(key, val);
      // }
      console.log(combined.toString());
      console.log(this.paginationParams.toString());
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
    this.paginationParams.append('ordering', 'created_at');
    this.registrationFilterParams = new URLSearchParams();
  },
  watch: {
    options: {
      handler() {
        const {
          sortBy,
          sortDesc,
          page,
        } = this.options;

        const pageParams = new URLSearchParams();
        // pageParams.append('page-size', itemsPerPage);
        pageParams.append('page-size', '-1');
        pageParams.append('page', page);

        console.log(sortBy);
        if (sortBy) {
          const ordering = (sortDesc[0] ? '-' : '') + sortBy[0];
          pageParams.append('ordering', ordering);
          console.log(ordering);
        } else {
          pageParams.append('ordering', 'lastName');
        }

        this.paginationParams = pageParams;
        this.getData();
      },
      deep: true,
    },
  },
};
</script>
