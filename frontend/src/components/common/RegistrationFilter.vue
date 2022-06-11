<template>
  <v-container>
    <v-row class="center text-center justify-center pa-0">
      <v-col cols="6">
        <v-checkbox
            label="Nur Bestätigt"
            @change="onFilterSelected"
            hide-details
            v-model="justConfirmed"/>
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
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  props: {
    value: {
      default: null,
    },
    eventId: {
      required: true,
    },
  },
  data() {
    return {
      selectedBookingOption: [],
      bookingOptionList: [],
      loading: false,
      justConfirmed: true,
    };
  },
  methods: {
    onFilterSelected() {
      const param = new URLSearchParams();
      param.append('confirmed', this.justConfirmed);
      if (this.selectedBookingOption) {
        this.selectedBookingOption.forEach((value) => {
          param.append('booking-option', value);
        });
      }
      this.$emit('onFilterSelected', param);
    },
    getData() {
      this.loading = true;

      this.getBookingOptions(this.eventId)
        .then((result) => {
          this.bookingOptionList = result.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>

<style>
</style>
