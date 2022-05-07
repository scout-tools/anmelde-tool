<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center pa-0">
      <v-card class="mx-auto pa-0" flat>
          <v-container class="pa-0" fluid>
            <v-row>
              <v-col cols="12"  sm="4">
                <kpi-card :data="kpiCardOne" color="blue darken-1" />
              </v-col>
               <v-col cols="12"  sm="4">
                <kpi-card :data="kpiCardTwo" color="green darken-1" />
               </v-col>
               <v-col cols="12" sm="4">
                <kpi-card :data="kpiCardThree" color="red darken-1" />
                </v-col>
            </v-row>
          </v-container>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import serviceMixin from '@/mixins/serviceMixin';
import kpiCard from '@/components/kpi/Card.vue';

export default {
  mixins: [serviceMixin],
  components: {
    kpiCard,
  },
  data: () => ({
    data: [],
  }),
  computed: {
    ...mapGetters([]),
    eventId() {
      return this.$route.params.id;
    },
    kpiCardOne() {
      return {
        header: 'Teilnehmer',
        subheader: 'Anzahl',
        dataOne: this.data.totalParticipants,
        dataOneName: '',
      };
    },
    kpiCardTwo() {
      return {
        header: 'Normal',
        subheader: 'Anzahl',
        dataOne: this.data.noHabits,
        dataOneName: '',
      };
    },
    kpiCardThree() {
      return {
        header: 'Einschränkungen',
        subheader: 'Anzahl',
        dataOne: this.data.eatHabits,
        dataOneName: '',
      };
    },
  },
  methods: {
    getData(eventId) {
      this.getFoodSummary(eventId).then((responseObj) => {
        this.data = responseObj.data; // eslint-disable-line
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
