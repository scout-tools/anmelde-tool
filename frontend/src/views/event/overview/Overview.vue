<template>
  <div>
    <v-card v-if="hasSetExtendedUserInfos" max-width="600" class="mx-auto">
      <v-card-title class="text-center justify-center py-6">
        Zu diesen Veranstaltungen kannst du dich Anmelden:
      </v-card-title>
      <v-list subheader two-line>
        <v-subheader inset
          >Hier kannst du alle deine aktuell Buchbaren Veranstaltungen sehen</v-subheader
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
                  <v-icon fab large color="primary">
                    mdi-account-multiple-plus
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
    getData() {
      const path = `${this.API_URL}basic/event/`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
      const userExtendedPath = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`;
      axios
        .get(userExtendedPath)
        .then((res) => {
          this.userExtendedItems = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
    onRegistrationClicked() {
      this.$router.push({ name: 'registrationForm' });
    },
  },
  created() {
    this.getData();
  },
};
</script>
