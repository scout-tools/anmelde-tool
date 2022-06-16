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
    <v-row v-if="!loading && data" justify="center" class="overflow-y: auto">
      <v-data-table
          :items="getPersons"
          :items-per-page="itemsPerPage"
          :expanded.sync="expanded"
          :headers="headers"
          show-expand
          single-expand
          item-key="createdAt">
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
      </v-data-table>
    </v-row>
    <v-row v-if="!loading && !data" justify="center">
      <p>Bitte wähle einen Stamm</p>
    </v-row>
    <v-row v-if="loading" justify="center">
      <div class="text-center ma-5">
        <p>Lade Daten ...</p>
        <v-progress-circular
            :size="80"
            :width="10"
            class="ma-5"
            color="primary"
            indeterminate/>
        <p>Bitte hab etwas Geduld.</p>
      </div>
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
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getPersons() {
      const result = [];
      this.data.map((x) => x.participants).forEach((item) => {
        item.forEach((person) => {
          result.push(person);
        });
      });
      return result;
    },
  },
  methods: {
    onFilterSelected(params) {
      this.getData(params);
    },
    getData(param) {
      this.loading = true;
      this.getRegistrationSummaryDetails(this.eventId, param)
        .then((result) => {
          this.data = result.data;
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
    // this.getData();
  },
};
</script>
