<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center pa-0">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardOne" color="red lighten-1" />
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card :data="kpiCardTwo" color="blue lighten-1" />
              </v-col>
            </v-row>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
                <kpi-card-list :data="kpiCardThree" color="teal lighten-1" />
              </v-col>
              <v-col cols="12" md="6">
                <kpi-card-list
                  :data="kpiCardFour"
                  color="light-green lighten-1"
                />
              </v-col>
            </v-row>
            <v-row>
              <v-col
                :cols="12 / bookingOptions.length" v-for="(item, i) in bookingOptions" :key="i">
                <kpi-card :data="bookingOptionData(item)" color="orange darken-1" />
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
import kpiCardList from '@/components/kpi/CardList.vue';
import kpiCard from '@/components/kpi/Card.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    kpiCard,
    kpiCardList,
  },
  data: () => ({
    data: [],
  }),
  computed: {
    ...mapGetters([]),
    bookingOptions() {
      if (this.data && this.data.bookingOptions && this.data.bookingOptions.length) {
        return this.data.bookingOptions.filter((item) => item.count);
      }
      return [];
    },
    eventId() {
      return this.$route.params.id;
    },
    confirmedData() {
      if (this.data && this.data.registrationSet) {
        return this.data.registrationSet.filter((item) => item.isConfirmed);
      }
      return [];
    },
    kpiCardOne() {
      return {
        header: 'Anmeldungen',
        subheader: 'Anzahl Personen',
        dataOne: this.confirmedData.reduce(
          (accum, item) => accum + item.participantCount,
          0,
        ),
        dataOneName: '',
      };
    },
    kpiCardTwo() {
      return {
        header: 'Anmeldungen',
        subheader: 'Anzahl Stämme',
        dataOne: this.confirmedData.length,
        dataOneName: '',
      };
    },
    kpiCardThree() {
      return {
        header: 'Letzen Anmeldungen',
        dataOne: this.sortByKey(this.confirmedData, 'createdAt'),
        subheader: 'Nach Bestätigundsdatum',
        rankField: 'updatedAt',
        rankOrder: 'desc',
      };
    },
    kpiCardFour() {
      return {
        header: 'Größte Anmeldungen',
        subheader: 'nach Gesamtteilnehmer',
        dataOne: this.confirmedData,
        rankField: 'participantCount',
        rankOrder: 'desc',
      };
    },
  },
  methods: {
    bookingOptionData(item) {
      return {
        header: item.bookingOption,
        subheader: 'Personen',
        dataOne: item.count,
        dataOneName: '',
      };
    },
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0} (${item.numberHelper || 0})`;
    },
    getData(eventId) {
      this.getRegistrationSummary(eventId).then((responseObj) => {
        this.data = responseObj.data[0]; // eslint-disable-line
      });
    },
    sortByKey(array, key) {
      return array.sort((a, b) => {
        const x = a[key];
        const y = b[key];
        return x > y ? -1 : x < y ? 1 : 0; // eslint-disable-line
      });
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
