<template>
  <v-combobox
    v-model="model"
    :items="items"
    label="Essen"
    item-text="name"
    item-value="id"
    prepend-icon="mdi-food"
    return-object
    multiple
    clearable
    chips
  ></v-combobox>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    entries: [],
    isLoading: false,
    model: [],
    search: null,
  }),
  computed: {
    ...mapGetters(['eatHabitTypeMapping']),

    items() {
      if (!this.model.filter((item) => item.id === 2).length) {
        return this.eatHabitTypeMapping;
      }
      return this.eatHabitTypeMapping
        .filter((item) => item.id !== 5)
        .filter((item) => item.id !== 6)
        .filter((item) => item.id !== 1);
    },
  },
};
</script>
