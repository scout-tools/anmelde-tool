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
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import serviceMixin from '@/mixins/serviceMixin';
import kpiCardList from '@/components/kpi/CardList.vue';
import kpiCard from '@/components/kpi/Card.vue';

export default {
  mixins: [serviceMixin],
  components: {
    kpiCard,
    kpiCardList,
  },
  data: () => ({
    data: [],
  }),
  computed: {
    ...mapGetters([
      'myStamm',
      'myBund',
    ]),
    eventId() {
      return this.$route.params.id;
    },
    confirmedData() {
      return this.data.filter((item) => item.isConfirmed);
    },
    getBundData() {
      return this.data.filter((item) => item.bundName === this.myBund);
    },
    kpiCardOne() {
      return {
        header: 'Anmeldungen',
        subheader: 'Bestätigt',
        dataOne: this.confirmedData.reduce(
          (accum, item) => accum + item.numberParticipant,
          0,
        ),
        dataTwo: this.getBundData.reduce(
          (accum, item) => accum + item.numberParticipant,
          0,
        ),
        dataOneName: 'DPV',
        dataTwoName: 'Eigener Bund',
      };
    },
    kpiCardTwo() {
      return {
        header: 'Anzahl Stämme',
        subheader: 'aus den Bünden',
        dataOne: this.confirmedData.length,
        dataTwo: this.getBundData.length,
        dataOneName: 'DPV',
        dataTwoName: 'Eigener Bund',
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
        rankField: 'numberParticipant',
        rankOrder: 'desc',
      };
    },
  },
  methods: {
    getNumberParticipant(item) {
      return `${item.numberParticipant || 0} (${item.numberHelper || 0})`;
    },
    getData(eventId) {
      this.getRegistrationSummary(eventId).then((responseObj) => {
        this.data = responseObj.data;
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
