<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center pa-0">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardOne" color="red lighten-1"/>
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardTwo" color="blue lighten-1"/>
              </v-col>
            </v-row>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardThree" color="teal lighten-1"/>
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card
                    :data="kpiCardFour"
                    color="light-green lighten-1"/>
              </v-col>
            </v-row>
            <v-row>
              <v-col
                  :cols="4"
                  v-for="(item, i) in bookingOptions"
                  :key="i">
                <kpi-card
                    :data="bookingOptionData(item)"
                    color="orange darken-1"/>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import kpiCard from '@/components/kpi/Card.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    kpiCard,
  },
  data: () => ({
    data: [],
    loading: true,
    bookingOptions: [],
  }),
  computed: {
    ...mapGetters([]),
    eventId() {
      return this.$route.params.id;
    },
    kpiCardOne() {
      return {
        header: 'Anmeldungen',
        subheader: 'Anzahl Personen',
        lookUpPath: `/event/event/${this.eventId}/summary/kpi/total-participants/`,
        dataOneName: '',
        fieldType: 'card',
      };
    },
    kpiCardTwo() {
      return {
        header: 'Anmeldungen',
        subheader: 'Anzahl Stämme',
        lookUpPath: `/event/event/${this.eventId}/summary/kpi/total-registrations/`,
        dataOneName: '',
        fieldType: 'card',
      };
    },
    kpiCardThree() {
      return {
        header: 'Letzen Anmeldungen',
        lookUpPath: `/event/event/${this.eventId}/summary/kpi/last-registrations/`,
        subheader: 'Nach Bestätigundsdatum',
        rankField: 'updatedAt',
        fieldType: 'list',
      };
    },
    kpiCardFour() {
      return {
        header: 'Größte Anmeldungen',
        subheader: 'nach Gesamtteilnehmer',
        lookUpPath: `/event/event/${this.eventId}/summary/kpi/largest-registrations/`,
        rankField: 'participantCount',
        fieldType: 'list',
      };
    },
  },
  methods: {
    bookingOptionData(item) {
      return {
        header: item.name,
        subheader: 'Personen',
        dataOneName: '',
        lookUpPath: `/event/event/${this.eventId}/summary/kpi/booking-options/?booking-option=${item.id}`,
        fieldType: 'card',
      };
    },
    getData() {
      this.loading = true;

      this.getBookingOptions(this.eventId)
        .then((result) => {
          this.bookingOptions = result.data;
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
