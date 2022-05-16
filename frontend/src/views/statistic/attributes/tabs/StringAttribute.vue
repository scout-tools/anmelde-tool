<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-container class="pa-0" fluid>
          <v-card-title>
            {{ attribute.title }}
          </v-card-title>
          <v-card-subtitle>
            {{ attribute.text }}
          </v-card-subtitle>
        </v-container>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table
        :headers="headers"
        :items="getItems"
        :items-per-page="itemsPerPage"
        :expanded.sync="expanded"
        show-expand
        single-expand
        hide-default-footer
        item-key="tag.id">
        <template v-slot:[`item.persons`]="{ item }">
          {{ getResponsiblePersonsText(item) }}
        </template>
        <template v-slot:expanded-item="{ item }">
          <pre style="word-break: break-word" class="text-wrap">
            {{ item.tag.stringField }}
          </pre>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>

export default {
  props: ['attribute'],
  data: () => ({
    headers: [
      {
        text: 'Name',
        value: 'tag.name',
      },
      {
        text: 'Ansprechperson(en)',
        value: 'persons',
      },
      {
        text: 'Stamm',
        value: 'registration.scoutOrganisation.name',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    itemsPerPage: 1000,
    expanded: [],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    getItems() {
      return this.attribute.attributes.data;
    },
  },

  methods: {
    getResponsiblePersonsText(item) {
      return item.registration.responsiblePersons.map((x) => x.userextended.scoutName).join(', ');
    },
  },
};
</script>
