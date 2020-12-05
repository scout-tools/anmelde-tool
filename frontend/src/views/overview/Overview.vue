<template>
  <v-data-table
    :headers="headers"
    :items="getItems"
    :items-per-page="5"
  >
    <!--<template v-slot:item.action="{ item }">
      <v-icon
        class="mr-2"
        @click="show(item)"
      >
        mdi-eye
      </v-icon>
    </template>-->
  </v-data-table>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    messages: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt/Lager', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      // { text: 'Actions', value: 'action', sortable: false },
    ],
    examples: [
      { id: 1, name: 'Ringlager', description: 'ganz toll' },
    ],
  }),

  computed: {
    getItems() {
      // this.messages.forEach((value) => console.log(value));
      return this.messages;
    },
  },
  methods: {
    onRefreshMessages() {
      this.messages = [];
      this.getMessages();
    },
    getMessages() {
      const path = `${this.API_URL}basic/event/`;
      axios.get(path)
        .then((res) => {
          this.showSuccess = true;
          this.messages = res.data;
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getMessages();
  },
  mounted() {
    this.getMessages();
  },
};
</script>
