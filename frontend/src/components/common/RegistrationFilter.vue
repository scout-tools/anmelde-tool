<template>
  <v-container>
    <v-row class="center text-center justify-center pa-0">
      <v-col cols="6">
        <v-checkbox
            label="Nur Bestätigt"
            @change="onFilterSelected"
            hide-details
            v-model="confirmed"/>
      </v-col>
      <v-col cols="6">
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
            v-model="selectedBookingOption"/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    value: {
      default: null,
    },
    bookingOptionList: [],
    loading: {
      default: false,
    },
    justConfirmed: {
      default: true,
    },
  },
  data() {
    return {
      selectedBookingOption: [],
      confirmed: this.justConfirmed,
    };
  },
  methods: {
    onFilterSelected() {
      const param = new URLSearchParams();
      param.append('confirmed', this.confirmed);
      if (this.selectedBookingOption) {
        this.selectedBookingOption.forEach((value) => {
          param.append('booking-option', value);
        });
      }
      this.$emit('onFilterSelected', param);
    },
  },
};
</script>

<style>
</style>
