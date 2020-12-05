<template>
  <v-btn
    class="mx-2"
    fab
    dark
    color="indigo"
  >
    <v-icon dark>
      mdi-plus
    </v-icon>
  </v-btn>
</template>
<template>
  <v-data-table
    :headers="headers"
    :items="examples"
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
  data() {
    return {
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
    };
  },

  methods: {
    getMessages() {
      const path = `${this.API_URL}basic/message?&timestamp=${new Date().getTime()}`;
      axios.get(path)
        .then((res) => {
          this.showSuccess = true;
          this.messages = res.data;
        })
        .catch(() => {
          this.showError = true;
        });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
  },
};
</script>
