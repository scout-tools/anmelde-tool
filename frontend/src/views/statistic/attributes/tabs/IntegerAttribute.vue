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
        hide-default-footer
        item-key="id">
         <template slot="body.append">
          <tr>
            <th>Summe</th>
            <th>{{ getTotalAttribute }}</th>
          </tr>
        </template>
      </v-data-table>
    </v-row>
  </v-container>
</template>

<script>
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment'; // eslint-disable-line

export default {
  mixins: [serviceMixin],
  props: ['attribute'],
  data: () => ({
    headers: [
      {
        text: 'Name',
        value: 'tag.name',
      },
      {
        text: 'Stamm',
        value: 'registration.scoutOrganisation.name',
      },
      {
        text: 'Anzahl',
        value: 'tag.integerField',
      },
    ],
    API_URL: process.env.VUE_APP_API,
    itemsPerPage: 1000,
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
    getTotalAttribute() {
      return this.attribute.attributes.sum;
    },
  },

  methods: {},
};
</script>
