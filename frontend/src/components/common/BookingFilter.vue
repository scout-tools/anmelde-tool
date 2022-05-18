<template>
  <v-autocomplete
    clearable
    :loading="loading"
    :items="bookingOptionList"
    :value="value"
    label="Filter nach Buchoptionen"
    multiple
    item-text="name"
    item-value="id"
    @change="onFilterSelected"
    no-data-text="Keine Buchoptionen gefunden."
  />
</template>

<script>
export default {
  props: {
    value: {
      default: null,
    },
    bookingOptionList: [],
    loading: {
      default: true,
    },
  },
  methods: {
    onFilterSelected(value) {
      this.$emit('onFilterSelected', value);
    },
  },
};
</script>

<style>
</style>
