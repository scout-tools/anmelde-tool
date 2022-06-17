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
      <v-card flat v-if="!loading">
        <v-data-table
            :headers="headers"
            :items="data"
            :items-per-page="itemsPerPage"
            hide-default-footer
            no-data-text="Keine Teilnehmer.">
        </v-data-table>
      </v-card>
      <v-card v-else flat>
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
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import RegistrationFilter from '@/components/common/RegistrationFilter.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    RegistrationFilter,
  },
  data: () => ({
    headers: [
      {
        text: 'Besonderheit',
        value: 'food',
      },
      {
        text: 'Personenanzahl',
        value: 'sum',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    showError: false,
    data: [],
    itemsPerPage: 1000,
    loading: false,
  }),

  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getData(param) {
      this.loading = true;

      this.getFoodSummary(this.eventId, param)
        .then((result) => {
            this.data = result.data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected(param) {
      this.getData(param);
    },
  },
  created() {
    const param = new URLSearchParams();
    param.append('confirmed', 'true');
    this.getData(param);
  },
};
</script>
