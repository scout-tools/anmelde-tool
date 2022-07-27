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
    </v-row>
    <v-row class="ma-0">
      <v-col cols="auto" md="4">
        <v-autocomplete
            :loading="loading"
            :items="stammList"
            v-model="selectedStamm"
            item-value="id"
            item-text="name"
            label="Filter nach Stamm/Stämmen"
            clearable
            multiple
            @change="onFilterSelected"
            no-data-text="Keine Stämme gefunden."/>
      </v-col>
      <v-col cols="auto" md="4">
        <v-autocomplete
            :loading="loading"
            :items="ringList"
            v-model="selectedRing"
            item-value="id"
            item-text="name"
            label="Filter nach Ring(en)"
            clearable
            multiple
            @change="onFilterSelected"
            no-data-text="Keine Ring(e) gefunden."/>
      </v-col>
      <v-col cols="auto" md="4">
        <v-autocomplete
            :loading="loading"
            :items="bundList"
            v-model="selectedBund"
            item-value="id"
            item-text="name"
            label="Filter nach Bund/Bünden"
            clearable
            multiple
            @change="onFilterSelected"
            no-data-text="Keine Bünde gefunden."/>
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
      selectedRing: [],
      ringList: [],
      selectedBund: [],
      bundList: [],
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

      if (this.selectedRing) {
        this.selectedRing.forEach((value) => {
          param.append('ring', value);
        });
      }

      if (this.selectedBund) {
        this.selectedBund.forEach((value) => {
          param.append('bund', value);
        });
      }

      this.$emit('onFilterSelected', param);
    },
    getData() {
      this.loading = true;

      const paramStaemmeList = new URLSearchParams();
      paramStaemmeList.append('level', '5');

      const paramRingList = new URLSearchParams();
      paramRingList.append('level', '4');

      const paramBundList = new URLSearchParams();
      paramBundList.append('level', '3');

      Promise.all([
        this.getBookingOptions(this.eventId),
        this.getParentOrganistations(this.eventId, paramStaemmeList),
        this.getParentOrganistations(this.eventId, paramRingList),
        this.getParentOrganistations(this.eventId, paramBundList),
      ])
        .then((values) => {
          this.bookingOptionList = values[0].data;
          this.stammList = values[1].data;
          this.ringList = values[2].data;
          this.bundList = values[3].data;
          if (this.preSelectStamm && this.selectedStamm.length === 0 && this.stammList.length > 0) {
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
