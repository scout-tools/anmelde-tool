<template>
  <v-autocomplete
    v-model="model"
    :items="items"
    :loading="isLoading"
    :search-input.sync="search"
    :item-text="customText"
    item-value="id"
    label="Stadt / Postleitzahl"
    placeholder="Wähle Stadt oder Postleitzahl"
    prepend-icon="mdi-city"
    return-object
  >
    <template slot="append">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="success" dark v-bind="attrs" v-on="on">
            mdi-help-circle-outline
          </v-icon>
        </template>
        <span>
          {{ tooltip }}
        </span>
      </v-tooltip>
    </template></v-autocomplete
  >
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    entries: [],
    isLoading: false,
    model: null,
    search: null,
    tooltip: 'Gebe die Stadt oder die Postleitzahl passend zur Adresse ein.',
  }),
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
  },
  computed: {
    items() {
      return this.entries;
    },
  },

  watch: {
    search() {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      // Lazily load input items
      const path = `${this.API_URL}basic/zip-code/`;
      axios
        .get(path)
        .then((res) => {
          this.count = res.data.length;
          this.entries = res.data;
          this.isLoading = false;
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
