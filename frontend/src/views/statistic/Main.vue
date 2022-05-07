<template>
  <v-container class="mt-10">
    <v-row justify="center" class="mt-5">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card>
            <v-tabs
              v-model="tab"
              background-color="primary"
              grow
              centered
              dark
              icons-and-text
            >
              <v-tabs-slider></v-tabs-slider>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-1">
                Übersicht
                <v-icon>mdi-clipboard-list</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-2">
                Leitung
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-3">
                Team
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-4">
                Essen
                <v-icon>mdi-food</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-5">
                Karte
                <v-icon>mdi-map</v-icon>
              </v-tab>

              <v-tab v-if="hasSubscribeWorkshop" href="#tab-6">
                Erlebnisangebot
                <v-icon>mdi-run-fast</v-icon>
              </v-tab>

              <v-tab v-if="hasAttributes" href="#tab-7">
                Attribute
                <v-icon>mdi-ticket</v-icon>
              </v-tab>

            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="i in 7" :key="i" :value="'tab-' + i">
                <v-card-text>
                  <OverviewMain v-if="hasParticipantsPersonal && i === 1"/>
                  <LeaderMain v-if="hasParticipantsPersonal && i === 2"/>
                  <TeamMain v-if="hasParticipantsPersonal && i === 3"/>
                  <FoodMain v-if="hasParticipantsPersonal && i === 4"/>
                  <MapsMain v-if="hasParticipantsPersonal && i === 5"/>
                  <WorkshopMain v-if="hasSubscribeWorkshop && i === 6"/>
                  <AttributeMain v-if="hasAttributes && i === 7"/>
                  <!-- <PdfGenerationMain v-if="i === 6"/> -->
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import OverviewMain from './overview/Main.vue';
import LeaderMain from './leader/Main.vue';
import TeamMain from './team/Main.vue';
import MapsMain from './maps/Main.vue';
import WorkshopMain from './workshop/Main.vue';
import AttributeMain from './attributes/Main.vue';
import FoodMain from './food/Main.vue';
// import PdfGenerationMain from './downlaods/Main.vue';

export default {
  components: {
    MapsMain,
    LeaderMain,
    TeamMain,
    WorkshopMain,
    // PdfGenerationMain,
    OverviewMain,
    AttributeMain,
    FoodMain,
  },
  mixins: [apiCallsMixin],
  computed: {
    ...mapGetters([]),
    eventId() {
      return this.$route.params.id;
    },
  },
  data() {
    return {
      tab: 1,
      eventOverview: [],
      hasParticipantsPersonal: false,
      hasSubscribeWorkshop: false,
      hasAttributes: false,
    };
  },
  methods: {
    getData() {
      const eventId = this.$route.params.id;
      this.loading = true;
      Promise.all([this.getAssignedEventModules(eventId)])
        .then((values) => {
          this.currentModules = values[0].data; // eslint-disable-line
          this.hasParticipantsPersonal = this.hasModule(this.currentModules, [
            'ParticipantsPersonal',
            'ParticipantsPersonalGold',
            'ParticipantsPersonalSmall',
            'ParticipantsPersonalPfingsten',
            'Participants',
          ]);
          this.hasSubscribeWorkshop = this.hasModule(this.currentModules, [
            'SubscribeWorkshop',
          ]);
          this.hasAttributes = true;
          this.loading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
    hasModule(currentModules, name) {
      return (
        currentModules && // eslint-disable-line
        currentModules.length && // eslint-disable-line
        currentModules.some(
          // eslint-disable-line
          (module) => name.includes(module.module.name), // eslint-disable-line
        )
      );
    },
    loadData() {
      this.getData();
    },
  },
  created() {
    this.loadData();
  },
};
</script>
