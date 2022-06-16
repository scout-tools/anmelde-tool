<template>
  <v-container>
    <v-row class="center text-center justify-center pa-0">
      <v-col cols="auto" md="3">
        <v-checkbox
            label="Nur Bestätigt"
            @change="onFilterSelected"
            hide-details
            v-model="justConfirmed"/>
      </v-col>
      <v-col cols="auto" md="4">
        <v-autocomplete
            clearable
            :loading="loading"
            :items="bookingOptionList"
            label="Filter nach Buchoptionen"
            multiple
            item-text="name"
            item-value="id"
            @change="onFilterSelected"
            no-data-text="Keine Buchoptionen gefunden."
            v-model="selectedBookingOption"/>
      </v-col>
      <v-col cols="auto" md="4">
        <v-autocomplete
            :loading="loading"
            :items="stammList"
            v-model="selectedStamm"
            item-value="id"
            item-text="name"
            label="Filter nach Stämmen"
            clearable
            multiple
            @change="onFilterSelected"
            no-data-text="Keine Buchoptionen gefunden."/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  props: {
    eventId: {
      required: true,
    },
    preSelectStamm: {
      default: false,
    },
  },
  data() {
    return {
      selectedBookingOption: [],
      bookingOptionList: [],
      loading: false,
      justConfirmed: true,
      selectedStamm: [],
      stammList: [],
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

      if (this.selectedStamm) {
        this.selectedStamm.forEach((value) => {
          param.append('stamm', value);
        });
      }
      this.$emit('onFilterSelected', param);
    },
    getData() {
      this.loading = true;

      Promise.all([
        this.getRegistrationStaemme(this.eventId),
        this.getBookingOptions(this.eventId),
      ])
        .then((values) => {
          this.bookingOptionList = values[1].data;
          this.stammList = values[0].data;
          if (this.preSelectStamm && this.selectedStamm.length === 0) {
            this.selectedStamm = [this.stammList[0].id];
            this.onFilterSelected();
          }
        })
        .catch((err) => {
          this.$root.globalSnackbar.show({
            message: err.data,
            color: 'error',
          });
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
