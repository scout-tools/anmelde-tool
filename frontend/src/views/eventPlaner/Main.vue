<template>
  <v-container class="top-margin my-12">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!isLoading">
            <v-card-title class="text-center justify-center my-6">
              Diese Fahrten kannst du bearbeiten
            </v-card-title>
            <v-card-actions class="justify-center align-center">
              <v-btn
                x-large
                color="success"
                @click=createNewEvent>
                <v-icon left>mdi-calendar-plus</v-icon>
                Neue Fahrt erstellen
              </v-btn>
            </v-card-actions>
            <v-expansion-panels class="mt-3">
              <v-expansion-panel v-for="(item, index) in items" :key="index">
                <v-expansion-panel-header>
                  <v-list-item :key="item.name">
                    <v-list-item-avatar>
                      <v-icon
                        :class="'primary'"
                        dark
                        v-text="'mdi-tent'"/>
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title
                        v-text="item.name"
                      ></v-list-item-title>
                      <v-list-item-subtitle
                        v-text="item.description">
                      </v-list-item-subtitle>

                      <v-list-item-subtitle>
                        {{ getLagerText(item) }}
                      </v-list-item-subtitle>

                      <v-list-item-subtitle>
                        {{ getDeadline(item) }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-row
                    v-for="(editItem,editIndex) in orderEventModules(item.eventmodulemapperSet)"
                    :key="editIndex">
                    <v-btn @click="editEvent(editIndex+1,item.id)"
                           color="blue-grey"
                           class="ma-2 white--text">
                      <v-icon dark color="primary"> mdi-pencil</v-icon>
                      {{ editItem.module.header }}
                    </v-btn>
                  </v-row>
                  <v-row>
                    <v-btn class="ma-2" color="primary" @click="editCompleteEvent(item.id)">
                      Bearbeite das ganze Event
                    </v-btn>
                  </v-row>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
          <v-card v-else>
            <div class="text-center ma-5">
              <p>Lade Daten ...</p>
              <v-progress-circular
                :size="80"
                :width="10"
                class="ma-5"
                color="primary"
                indeterminate
              ></v-progress-circular>
              <p>Bitte hab etwas Geduld.</p>
            </div>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import moment from 'moment';
import { orderBy } from 'lodash';

export default {
  name: 'Main',
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    isLoading: true,
  }),
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
  },
  methods: {
    async getEventPlanerOverview() {
      const path = `${this.API_URL}/event/event-planer-overview/`;
      const response = await axios.get(path);
      return response;
    },
    getLagerText(item) {
      const startTime = new Date(item.startTime);
      const endTime = new Date(item.endTime);
      return `Termin: ${moment(startTime, 'll', 'de')
        .format('ll')} bis
      ${moment(endTime, 'll', 'de')
    .format('ll')}`;
    },
    getDeadline(item) {
      const registrationDeadline = new Date(item.registrationDeadline);
      return `Anmeldeschluss: ${moment(registrationDeadline, 'll', 'de')
        .format('ll')}`;
    },
    createNewEvent() {
      axios.post(`${this.API_URL}/event/event/`)
        .then((success) => {
          const newEventId = success.data.id;
          this.$router.push({
            name: 'planEvent',
            params: { id: newEventId },
          });
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim erstellen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
        });
    },
    editEvent(step, eventId) {
      this.$router.push({
        name: 'planEvent',
        params: {
          step,
          id: eventId,
        },
      });
    },
    editCompleteEvent(eventId) {
      this.$router.push({
        name: 'planEvent',
        params: {
          id: eventId,
        },
      });
    },
    orderEventModules(eventModules) {
      return orderBy(eventModules, 'position');
    },
  },
  created() {
    this.getEventPlanerOverview()
      .then((respone) => {
        this.items = respone.data;
      })
      .finally(() => {
        this.isLoading = false;
      });
  },
};
</script>

<style scoped>

</style>
