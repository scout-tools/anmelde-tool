<template>
  <v-autocomplete
    v-model="model"
    :items="items"
    :loading="isLoading"
    :search-input.sync="search"
    :item-text="customText"
    item-value="id"
    label="Postleitzahl"
    placeholder="Gebe die Postleitzahl aus"
    prepend-icon="mdi-city"
    return-object
  ></v-autocomplete>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    entries: [],
    isLoading: false,
    model: null,
    search: null,
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
      axios
        .get('http://localhost:8000/basic/zip-code/')
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
