<template>
  <v-container fluid class="pa-0">
    <v-row justify="center" class="overflow-y: auto ma-3">
      <v-data-table
        :headers="headers"
        :items="getItems()"
        show-expand
        hide-default-footer
      >
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ moment(item.createdAt).format('DD.MM.YYYY') }}
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
                <h4>Workshop</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  Titel: {{ item.title }}
                  <br />
                  <br />
                  Kosten: {{ item.price }} €
                  <br />
                  <br />
                  von {{ item.minPerson }} bis {{ item.maxPerson }} Personen
                </p>
              </v-row>
              <v-row>
                <h4>Kontakt</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  Name: {{ item.contactFirstname }} {{ item.contactLastname }}
                  <br />
                  <br />
                  Pfadfindername: {{ item.supervisor.userextended.scoutName }}
                  <br />
                  <br />
                  {{ item.supervisor.userextended.scoutOrganisation.name }} ({{
                    item.supervisor.userextended.scoutOrganisation.bund
                  }})
                  <br />
                  <br />
                  E-Mail: {{ item.supervisor.email }}
                  <br />
                  <br />
                  Nummer: {{ item.supervisor.userextended.mobileNumber }}
                  <br />
                  <br />
                </p>
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

export default {
  mixins: [apiCallsMixin],
  data: () => ({
    data: [],
    headers: [
      { text: 'AG-Name', value: 'title' },
      { text: 'Verantwortlicher', value: 'supervisor.userextended.scoutName' },
      { text: 'Bund', value: 'supervisor.userextended.scoutOrganisation.bund' },
      {
        text: 'Stamm',
        value: 'supervisor.userextended.scoutOrganisation.name',
      },
      { text: 'Datum', value: 'createdAt' },
    ],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getItems() {
      return this.data;
    },
    async getData() {
      const { data } = await this.getWorkshopSummary(this.eventId);
      this.data = data;
    },
  },
  created() {
    this.getData();
  },
};
</script>

<style scoped>
.w-75 {
  width: 75%;
}
</style>
