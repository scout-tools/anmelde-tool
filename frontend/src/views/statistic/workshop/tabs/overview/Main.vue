<template>
  <v-container fluid class="pa-0">
    <v-row justify="center" class="overflow-y: auto ma-3">
      <v-data-table
          :loading="isLoading"
          :headers="headers"
          :items="getItems()"
          show-expand
          hide-default-footer>
        <template v-slot:[`item.createdAt`]="{ item }">
          {{
            formatDate(item.createdAt)
          }}
        </template>
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <v-container class="ma-3">
              <v-row>
                <h4>Beschreibung</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  {{ item.freeText }}
                </p>
              </v-row>
              <v-row>
                <h4>Erlebnisangebot: {{ item.type }}</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  Titel: {{ item.title }}
                  <br/>
                  <br/>
                   Fixe Kosten: {{ item.price }}€
                  <br/>
                   Kosten pro Teilnehmer {{ item.pricePerPerson}}€
                  <br/>
                  <br/>
                  Dauer: {{item.duration}} Minuten
                  <br/>
                  <br/>
                  Kann wiederholt werden: {{ canBeRepeatedText(item.canBeRepeated)}}
                </p>
              </v-row>
              <v-row>
                <h4>Teilnehmer</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                 {{ item.minPerson }} bis {{ item.maxPerson }} Personen
                </p>
              </v-row>
              <v-row>
                <h4>Kontakt</h4>
              </v-row>
                <v-row v-if="item.supervisor.firstName && item.supervisor.lastName">
                  Name: {{ item.supervisor.firstName }} {{ item.supervisor.lastName }}
                </v-row>
                <v-row v-if="item.supervisor.userextended.scoutName">
                  Pfadfindername: {{ item.supervisor.userextended.scoutName }}
                </v-row>
                <v-row v-if="item.supervisor.userextended.scoutOrganisation">
                  {{ item.supervisor.userextended.scoutOrganisation.name }}
                  ({{ item.supervisor.userextended.scoutOrganisation.bund }})
                </v-row>
                <v-row v-if="item.supervisor.email">
                  E-Mail: {{ item.supervisor.email }}
                </v-row>
                <v-row v-if="item.supervisor.userextended.mobileNumber">
                  Nummer: {{ item.supervisor.userextended.mobileNumber }}
                </v-row>
                <v-row v-if="!getEmptyContact(item)">
                  Leider wurde kein Kontakt angegeben.
                </v-row>
            </v-container>
          </td>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment';

export default {
  mixins: [apiCallsMixin],
  data: () => ({
    data: [],
    headers: [
      {
        text: 'AG-Name',
        value: 'title',
      },
      {
        text: 'Verantwortlicher',
        value: 'supervisor.userextended.scoutName',
      },
      {
        text: 'Bund',
        value: 'supervisor.userextended.scoutOrganisation.bund',
      },
      {
        text: 'Stamm',
        value: 'supervisor.userextended.scoutOrganisation.name',
      },
      {
        text: 'Datum',
        value: 'createdAt',
      },
    ],
    isLoading: false,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getItems() {
      if (this.data) {
        return this.data;
      }
      return [];
    },
    getData() {
      this.isLoading = true;
      this.getWorkshopSummary(this.eventId)
        .then((success) => {
          this.data = success.data;
        })
        .catch((error) => {
          this.$root.globalSnackbar.show({
            message: error.response.data,
            color: 'error',
          });
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    formatDate(item) {
      return moment(item)
        .format('DD.MM.YYYY');
    },
    getEmptyContact(item) {
      return item.supervisor && item.supervisor.email && item.supervisor.mobileNumer;
    },
    canBeRepeatedText(item) {
      return item ? 'Ja' : 'Nein';
    },
  },
  created() {
    this.getData();
  },
};
</script>
