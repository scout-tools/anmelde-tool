<template>
  <v-container fluid class="pa-0">
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
        :headers="headers"
        :items="getItems()"
        show-expand
        class="w-75"
      >
        <!-- <template v-slot:item.costs="{ item }"> {{ item.costs }} € </template>  -->
        <template v-slot:expanded-item="{ headers, item }">
          <td :colspan="headers.length">
            <v-container>
              <v-row>
                <h4>Beschreibung</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  {{ item.workshopFreeText }}
                </p>
              </v-row>
              <v-row>
                <h4>Workshop</h4>
              </v-row>
              <v-row>
                <p class="pt-3">
                  Titel: {{ item.workshopTitle }}
                  <br />
                  <br />
                  Kosten: {{ item.workshopCosts }} €
                  <br />
                  <br />
                  von {{ item.workshopMinPerson }} bis
                  {{ item.workshopMaxPerson }} Personen
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
                  Pfadfindername: {{ item.contactScoutname }}
                  <br />
                  <br />
                  {{ item.scoutOrganisation}} ({{ item.bundName}})
                  <br />
                  <br />
                  E-Mail: {{ item.contactEmail }}
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
import { serviceMixin } from '@/mixins/serviceMixin';

export default {
  mixins: [serviceMixin],
  data: () => ({
    data: [],
    headers: [
      { text: 'AG-Name', value: 'workshopTitle' },
      { text: 'Verantwortlicher', value: 'contactScoutname' },
      { text: 'Bund', value: 'bundName' },
      { text: 'Stamm', value: 'scoutOrganisation' },
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
      const { data } = await this.getWorkshopStats(this.eventId);
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
