<template>
  <v-data-table
    :headers="headers"
    :items="getItems"
    :items-per-page="5"
  >
    <template v-slot:item.action="{ item }">
      <v-icon
        class="mr-2"
        @click="show(item)"
      >
        mdi-eye
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt/Lager', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
  }),

  computed: {
    getItems() {
      // this.messages.forEach((value) => console.log(value));
      return this.items;
    },
  },
  methods: {
    getData() {
      const path = `${this.API_URL}basic/event/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
