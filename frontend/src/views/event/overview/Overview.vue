<template>
  <div>
    <v-card v-if="hasSetExtendedUserInfos" max-width="600" class="mx-auto top-margin">
      <v-card-title class="text-center justify-center py-6">
        Zu diesen Veranstaltungen kannst du dich Anmelden:
      </v-card-title>
      <v-list subheader two-line>
        <v-subheader inset
          >Hier kannst du alle deine aktuell buchbaren Veranstaltungen sehen</v-subheader
        >
        <template v-for="(item, index) in getItems">
          <v-list-item :key="item.name">
            <v-list-item-avatar>
              <v-icon color="black">
                mdi-account-group</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title v-text="item.name"></v-list-item-title>

              <v-list-item-subtitle class="text--primary">
                {{ getText(item) }}
              </v-list-item-subtitle>

              <v-list-item-subtitle v-text="item.description"></v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-action>
              <router-link
                :to="{ name: 'registrationForm', params: { id: item.id } }"
                style="text-decoration: none"
              >
                <v-btn icon>
                  <v-icon fab color="primary">
                    mdi-account-multiple-plus
                  </v-icon>
                </v-btn>
              </router-link>
            </v-list-item-action>
            <v-list-item-action>
              <router-link
                :to="{ name: 'statisticOverview', params: { id: item.id } }"
                style="text-decoration: none"
                v-if="!isSimpleUser || item.participantRole.length"
              >
                <v-btn icon>
                  <v-icon fab color="primary">
                    mdi-chart-bar
                  </v-icon>
                </v-btn>
              </router-link>
            </v-list-item-action>
          </v-list-item>
          <v-divider v-if="index < getItems.length - 1" :key="index"></v-divider>
        </template>
      </v-list>
    </v-card>
    <v-card v-else max-width="600" class="mx-auto">
      <v-card-title class="text-center justify-center py-6">
        Bitte lege erst deinen Namen und deinen Stamm fest
      </v-card-title>
      <v-btn color="primary" class="ma-2" @click="$router.push({ name: 'settingsUser' })">
        Daten hinzufügen
        <v-icon right dark> mdi-tools </v-icon>
      </v-btn>
    </v-card>
  </div>
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
      return this.items;
    },
    hasSetExtendedUserInfos() {
      if (this.userExtendedItems) {
        return (
          this.userExtendedItems.scoutName && this.userExtendedItems.scoutOrganisation
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
    getText(item) {
      const startTime = new Date(item.startTime);
      const endTime = new Date(item.endTime);
      const dateFormat = 'll';

      return `${moment(startTime).format(dateFormat)} bis ${moment(endTime).format(
        dateFormat,
      )}`;
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
      const path = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/?&timestamp=${new Date().getTime()}`;
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

    getParticipantRoleMapping() {
      const path = `${this.API_URL}basic/participant-role/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setParticipantRoleMapping', res.data);
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
