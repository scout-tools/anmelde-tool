<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!loading">
            <v-card-title class="text-center justify-center py-6">
              Hier werden die Fahrten angezeigt, die du bearbeiten darfst.
            </v-card-title>
            <v-list subheader two-line>
              <v-subheader inset>
              </v-subheader>

              <v-btn
                class="ma-6"
                color="success"
                v-if="isAuthenticated"
                @click="$router.push({ name: 'createEvent' })"
              >
                <v-icon left>mdi-calendar-plus</v-icon>
                Neue Fahrt erstellen
              </v-btn>
              <v-divider/>
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

                    <v-list-item-subtitle
                      v-text="item.description"
                    ></v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getLagerText(item) }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getDeadline(item) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action
                    v-show="
                      isInTimeRange(
                        item.registrationStart,
                        item.registrationDeadline,
                      ) && isNotAlreadyRegistered(item)
                    "
                  >
                    <router-link
                      :to="{
                        name: 'registrationForm',
                        params: {
                          id: item.id,
                        },
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
                        <span>Fahrtenanmeldung</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>

                  <v-list-item-action>
                    <v-btn
                      icon
                      @click="onEventEditClicked(item.id)"
                    >
                      <v-icon fab color="primary"> mdi-pencil</v-icon>
                    </v-btn>
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
    <confirm-registration-edit-modal ref="confirmRegistrationEditModal"/>
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import { mapGetters } from 'vuex';
// eslint-disable-next-line import/extensions
import ConfirmRegistrationEditModal from '@/components/dialog/ConfirmRegistrationEditModal.vue';

export default {
  components: { ConfirmRegistrationEditModal },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    loading: true,
    userExtendedItems: [],
  }),

  computed: {
    ...mapGetters(['isAuthenticated']),
    getItems() {
      return this.items.filter((item) => item.canEdit);
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
    isStaff() {
      // if (this.getJwtData) {
      //   return this.getJwtData.isStaff;
      // }
      return false;
    },
  },
  methods: {
    isNotAlreadyRegistered() {
      return false;
    },
    onEventEditClicked(id) {
      this.$router.push({
        name: 'updateEvent',
        params: { id },
      });
    },
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
      const startDate = new Date(date1).getTime();
      const endDate = new Date(date2).getTime();
      const today = new Date().getTime();

      return today > startDate && today < endDate;
    },
    getLagerText(item) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);
      return `Termin: ${moment(startDate, 'll', 'de')
        .format('ll')} bis
      ${moment(endDate, 'll', 'de')
    .format('ll')}`;
    },
    getDeadline(item) {
      const registrationDeadline = new Date(item.registrationDeadline);
      const text2 = `Anmeldeschluss: ${moment(registrationDeadline, 'll', 'de')
        .format('ll')}`;
      return text2;
    },
    async getEvent() {
      const path = `${this.API_URL}basic/event-overview/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getUserExtended() {
      const { userId } = this.getJwtData;
      const ts = new Date().getTime();
      const path = `${this.API_URL}auth/data/user-extended/${userId}/?&timestamp=${ts}`;
      const response = await axios.get(path);

      return response.data;
    },
    async getRoleMapping() {
      const path = `${this.API_URL}basic/role/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getScoutOrgaLevelMapping() {
      const path = `${this.API_URL}basic/scout-orga-level/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getEatHabitTypeMapping() {
      const path = `${this.API_URL}basic/eat-habit-type/`;
      const response = await axios.get(path);

      return response.data;
    },

    async getTravelTypeMapping() {
      const path = `${this.API_URL}basic/travel-type/`;
      const response = await axios.get(path);

      return response.data;
    },

    async getHierarchyMapping() {
      const path = `${process.env.VUE_APP_API}basic/scout-hierarchy/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getAgeGroupMapping() {
      const path = `${this.API_URL}basic/age-group/`;
      const response = await axios.get(path);

      return response.data;
    },
    async getTentTypeMapping() {
      const path = `${this.API_URL}basic/tent-type/`;
      const response = await axios.get(path);

      return response.data;
    },
    onGoToSettingsButtonClicked() {
      this.goToSettings();
    },
    goToSettings() {
      this.$router.push({ name: 'settingsUser' });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
    onRegistrationClicked() {
      this.$router.push({ name: 'registrationForm' });
    },
  },
  mounted() {
    this.loading = true;

    Promise.all([
      this.getEvent(),
      this.getUserExtended(),
      this.getRoleMapping(),
      this.getScoutOrgaLevelMapping(),
      this.getEatHabitTypeMapping(),
      this.getTravelTypeMapping(),
      this.getHierarchyMapping(),
      this.getAgeGroupMapping(),
      this.getTentTypeMapping(),
    ])
      .then((values) => {
        [this.items, this.userExtendedItems] = values;

        this.$store.commit('setRoleMapping', values[2]);
        this.$store.commit('setScoutOrgaLevelMapping', values[3]);
        this.$store.commit('setEatHabitTypeMapping', values[4]);
        this.$store.commit('setTravelTypeTypeMapping', values[5]);
        this.$store.commit('setHierarchyMapping', values[6]);
        this.$store.commit('setAgeGroupMapping', values[7]);
        this.$store.commit('setTentTypeMapping', values[8]);

        if (!this.hasSetExtendedUserInfos) {
          this.goToSettings();
        }

        this.loading = false;
      })
      .catch((error) => {
        this.errormsg = error.response.data.message;
        this.loading = false;
      });
  },
};
</script>
