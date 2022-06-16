<template>
  <v-container class="mt-10">
    <v-row justify="center" class="mt-5" v-if="!error">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card>
            <v-tabs
                v-model="tab"
                background-color="primary"
                grow
                centered
                dark
                icons-and-text>
              <v-tabs-slider/>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-1">
                Übersicht
                <v-icon>mdi-clipboard-list</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal && isEventAdmin" href="#tab-2">
                Leitung
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal && !isEventAdmin && isLeader" href="#tab-3">
                Detailliert
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-4">
                Team
                <v-icon>mdi-counter</v-icon>
              </v-tab>

              <v-tab v-if="hasParticipantsPersonal" href="#tab-5">
                Karte
                <v-icon>mdi-map</v-icon>
              </v-tab>

              <v-tab v-if="hasAttributes && isEventPlaner" href="#tab-6">
                Attribute
                <v-icon>mdi-ticket</v-icon>
              </v-tab>

              <v-tab v-if="hasSubscribeWorkshop" href="#tab-7">
                Erlebnisangebot
                <v-icon>mdi-run-fast</v-icon>
              </v-tab>

            </v-tabs>
            <v-tabs-items v-model="tab">
              <v-tab-item v-for="i in 8" :key="i" :value="'tab-' + i">
                <v-card-text>
                  <OverviewMain v-if="hasParticipantsPersonal && i === 1"/>
                  <LeaderMain v-if="hasParticipantsPersonal && i === 2"/>
                  <BufueMain v-if="hasParticipantsPersonal && i === 3"/>
                  <TeamMain v-if="hasParticipantsPersonal && i === 4"/>
                  <MapsMain v-if="hasParticipantsPersonal && i === 5"/>
                  <AttributeMain v-if="hasAttributes && i === 6"/>
                  <WorkshopMain v-if="hasSubscribeWorkshop && i === 7"/>
                  <!-- <PdfGenerationMain v-if="i === 6"/> -->
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
    <v-row justify="center" class="ma-5" v-else>
      <v-container>
        <v-card>
          <div class="justify-center">
            <v-card-title primary-title class="justify-center red--text">
              Event nicht gefunden
            </v-card-title>
            <v-card-text>
              <br>Das Event mit der Id: <i>{{ eventId }}</i> konnte leider nicht gefunden werden.
              <br>Bitte überprüfe ob der Link richtig kopiert wurde/eingetippt wurde,
              <br>andernfalls wende dich bitte(!) an die Administratoren und beschreibe das Problem.
              <br>Das geht ganz schnell und einfach,
              wenn du unten rechts auf den Nachrichten Knopf drückst.
            </v-card-text>
          </div>
        </v-card>
      </v-container>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import OverviewMain from './overview/Main.vue';
import BufueMain from './leader/BufueMain.vue';
import LeaderMain from './leader/Main.vue';
import TeamMain from './team/Main.vue';
import MapsMain from './maps/Main.vue';
import WorkshopMain from './workshop/Main.vue';
import AttributeMain from './attributes/Main.vue';
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
    BufueMain,
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
      currentEventInfos: {},
      isEventPlaner: false,
      isEventAdmin: false,
      isLeader: false,
      error: false,
    };
  },
  methods: {
    getData() {
      const eventId = this.$route.params.id;
      this.loading = true;
      Promise.all([
        this.getAssignedEventModules(eventId),
        this.getEventOverviewById(eventId),

      ])
        .then((values) => {
            this.currentModules = values[0].data; // eslint-disable-line
          this.currentEventInfos = values[1].data;
          this.isEventAdmin = this.currentEventInfos.allowStatisticAdmin;
          this.isLeader = this.currentEventInfos.allowStatisticLeader;
          this.isEventPlaner = this.currentEventInfos.allowStatistic;
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
        })
        .catch((error) => {
          this.error = true;
          this.$root.globalSnackbar.show({
            message: error.response.data,
            color: 'error',
          });
        })
        .finally(() => {
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
