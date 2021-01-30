<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="hasSetExtendedUserInfos">
            <v-card-title class="text-center justify-center py-6">
              Zu diesen Lagern kannst du dich Anmelden:
            </v-card-title>
            <v-list subheader two-line>
              <v-subheader inset>
                Nicht lange zögern. Melde dich oder deine Gruppe zu einen dieser
                Lager an.
              </v-subheader>

              <v-btn
                class="ma-6"
                color="success"
                v-if="isAuthenticated && !isSimpleUser"
                @click="$router.push({ name: 'createEvent' })"
              >
                <v-icon left>mdi-calendar-plus</v-icon>
                Neues Lager
              </v-btn>

              <template v-for="(item, index) in getItems">
                <v-list-item :key="item.name">
                  <v-list-item-avatar>
                    <v-icon
                      :class="'primary'"
                      dark
                      v-text="'mdi-tent'"
                    ></v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title
                      v-text="getHeaderText(item.name, item.participantRole)"
                    ></v-list-item-title>

                    <v-list-item-subtitle class="text--primary">
                      {{ getLagerText(item) }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle
                      v-text="item.description"
                    ></v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action
                    v-show="
                      isInTimeRange(
                        item.registrationStart,
                        item.registrationDeadline,
                      ) && !item.isRegistered.length
                    "
                  >
                    <router-link
                      :to="{
                        name: 'registrationForm',
                        params: { id: item.id },
                      }"
                      style="text-decoration: none"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary">
                              mdi-account-multiple-plus
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Lageranmeldung</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>

                  <v-list-item-action
                    v-show="
                      isInTimeRange(
                        item.registrationStart,
                        item.registrationDeadline,
                      ) && item.isRegistered.length
                    "
                    class="ml-4"
                  >
                    <router-link
                      :to="{
                        name: 'registrationCreate',
                        params: { id: getRegisteredId(item) },
                      }"
                      style="text-decoration: none"
                      v-if="item.isRegistered.length"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary"> mdi-pencil </v-icon>
                          </v-btn>
                        </template>
                        <span>Lageranmeldung bearbeiten</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>

                  <v-list-item-action>
                    <router-link
                      :to="{
                        name: 'statisticOverview',
                        params: { id: item.id },
                      }"
                      style="text-decoration: none"
                      v-if="item.participantRole.length"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary"> mdi-chart-bar </v-icon>
                          </v-btn>
                        </template>
                        <span>Lagerstatistik</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>
                </v-list-item>
                <v-divider
                  v-if="index < getItems.length - 1"
                  :key="index"
                ></v-divider>
              </template>
            </v-list>
          </v-card>
          <v-card v-else>
            <v-card-title class="text-center justify-center py-6">
              Willkommen im Anmele-Tool
            </v-card-title>
            <v-subheader>
              Bevor du dich anmelden kannst musst du deine persönlichen Daten
              eingeben.
            </v-subheader>
            <v-btn
              class="ma-5"
              color="primary"
              @click="$router.push({ name: 'settingsUser' })"
            >
              <v-icon left dark>mdi-tools</v-icon>
              Zu den Benutzerdaten
            </v-btn>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    userExtendedItems: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt/Lager', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
  }),

  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    getItems() {
      console.log(this.items);
      return this.items;
    },
    hasSetExtendedUserInfos() {
      if (this.userExtendedItems) {
        return (
          this.userExtendedItems.scoutName && // eslint-disable-line
          this.userExtendedItems.scoutOrganisation
        );
      }
      return false;
    },
    isSimpleUser() {
      if (this.getJwtData) {
        return !(this.getJwtData.groups.length || this.getJwtData.isStaff);
      }
      return true;
    },
  },
  methods: {
    getHeaderText(header, roles) {
      if (roles && roles.length) {
        return `${header} (Deine Rolle: ${roles[0].eventRole_Name})`;
      }
      return header;
    },
    getRegisteredId(item) {
      if (
        item && // eslint-disable-line
        item.isRegistered && // eslint-disable-line
        item.isRegistered.length && // eslint-disable-line
        item.isRegistered[0].id
      ) {
        return item.isRegistered[0].id;
      }
      return 0;
    },
    isInTimeRange(date1, date2) {
      const startTime = new Date(date1).getTime();
      const endTime = new Date(date2).getTime();
      const today = new Date().getTime();

      return today > startTime && today < endTime;
    },
    getLagerText(item) {
      const startTime = new Date(item.startTime);
      const endTime = new Date(item.endTime);
      const registrationStart = new Date(item.registrationStart);
      const registrationDeadline = new Date(item.registrationDeadline);
      const dateFormat = 'll';

      const text1 = `Lager: ${moment(startTime)
        .lang('de')
        .format(dateFormat)} bis ${moment(endTime).lang('de').format(dateFormat)}`;

      const text2 = ` - Anmeldung: ${moment(registrationStart)
        .lang('de')
        .format(dateFormat)} bis ${moment(registrationDeadline).lang('de').format(
        dateFormat,
      )}`;
      return text1 + text2;
    },

    getEvent() {
      const path = `${this.API_URL}basic/event-overview/`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },

    getUserExtended() {
      this.userExtendedItems = [];
      const path = `${this.API_URL}auth/data/user-extended/${
        this.getJwtData.userId
      }/?&timestamp=${new Date().getTime()}`;
      axios
        .get(path)
        .then((res) => {
          this.userExtendedItems = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },

    getRoleMapping() {
      const path = `${this.API_URL}basic/role/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setRoleMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },

    getScoutOrgaLevelMapping() {
      const path = `${this.API_URL}basic/scout-orga-level/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setScoutOrgaLevelMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },

    getEatHabitTypeMapping() {
      const path = `${this.API_URL}basic/eat-habit-type/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setEatHabitTypeMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },

    getTravelTypeMapping() {
      const path = `${this.API_URL}basic/travel-type/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setTravelTypeTypeMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getHierarchyMapping() {
      const path = `${process.env.VUE_APP_API}basic/scout-hierarchy/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setHierarchyMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getAgeGroupMapping() {
      const path = `${this.API_URL}basic/age-group/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setAgeGroupMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getTentTypeMapping() {
      const path = `${this.API_URL}basic/tent-type/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setTentTypeMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },

    show(item) {
      this.$refs.messageModal.show(item);
    },
    onRegistrationClicked() {
      this.$router.push({ name: 'registrationForm' });
    },
  },
  mounted() {
    this.getEvent();
    this.getUserExtended();
    this.getScoutOrgaLevelMapping();
    this.getParticipantRoleMapping();
    this.getEatHabitTypeMapping();
    this.getTravelTypeMapping();
    this.getHierarchyMapping();
    this.getAgeGroupMapping();
    this.getTentTypeMapping();
  },
};
</script>
