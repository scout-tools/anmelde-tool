<template>
  <v-data-table
    :headers="headers"
    :items="getItems"
    :items-per-page="5"
    class="elevation-1"
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
    messages: [],
    headers: [
      {
        text: 'Fahrt/Lager',
        align: 'start',
        sortable: false,
        value: 'name',
      },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action' },
    ],
    examples: [
      {
        name: 'Ringfahrt',
        description: 'Dies ist eine Ringfahrt.',
      },
      {
        name: 'Ringfahrt2',
        description: 'Dies ist eine Ringfahrt2.',
      },
      {
        name: 'Ringfahrt3',
        description: 'Dies ist eine Ringfahrt3.',
      },
    ],
  }),

  computed: {
    getItems() {
      return this.messages;
    },
  },
  methods: {
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
    onRefreshMessages() {
      this.messages = [];
      this.getMessages();
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
  },
  beforeMount() {
    this.onRefreshMessages();
  },
};
</script>
