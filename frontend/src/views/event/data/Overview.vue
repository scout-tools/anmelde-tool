<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!isLoading">
            <v-card-title class="text-center justify-center py-6">
              Hier siehst du alle Fahrten zu denen du Daten freigegeben bekommen hast.
            </v-card-title>
            <v-list subheader two-line>
              <v-divider />
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

                  <v-list-item-action>
                    <router-link
                      :to="{
                        name: 'statisticOverview',
                        params: { id: item.id },
                      }"
                      style="text-decoration: none"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="primary"> mdi-chart-bar </v-icon>
                          </v-btn>
                        </template>
                        <span>Fahrtenstatistik</span>
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
    <confirm-registration-edit-modal ref="confirmRegistrationEditModal" />
  </v-container>
</template>

<script>
import axios from 'axios';
import moment from 'moment';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import ConfirmRegistrationEditModal from '@/components/dialog/ConfirmRegistrationEditModal.vue';

export default {
  components: { ConfirmRegistrationEditModal },
  mixins: [apiCallsMixin],
  data: () => ({
    components: {
      ConfirmRegistrationEditModal,
    },
    API_URL: process.env.VUE_APP_API,
    items: [],
    isLoading: true,
    userExtendedItems: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
  }),
  created() {
    this.getEventStatisticsOverview()
      .then((respone) => {
        this.items = respone.data;
      })
      .catch(() => {
        this.$root.globalSnackbar.show({
          message: 'Leider ist ein Problem beim anzeigen der Events aufgetreten, '
            + 'bitte probiere es später nocheinmal.',
          color: 'error',
        });
      })
      .finally(() => {
        this.isLoading = false;
      });
  },
  computed: {
    getItems() {
      return this.items;
    },
  },
  methods: {
    editRegistration(item) {
      this.$refs.confirmRegistrationEditModal.show(item);
    },
    getHeaderText(header, roles) {
      if (roles && roles.length) {
        return `${header} (Deine Rolle: ${roles[0].eventRole_Name})`;
      }
      return header;
    },
    getLagerText(item) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);
      const dateFormat = 'll';

      const text1 = `Termin: ${moment(startDate)
        .lang('de')
        .format(dateFormat)} bis ${moment(endDate)
        .lang('de')
        .format(dateFormat)}`;
      return text1;
    },
    getDeadline(item) {
      const dateFormat = 'll';
      const registrationDeadline = new Date(item.registrationDeadline);
      const text2 = `Anmeldeschluss: ${moment(registrationDeadline)
        .lang('de')
        .format(dateFormat)}`;
      return text2;
    },
    async getEvent() {
      const path = `${this.API_URL}basic/event-overview/`;
      const response = await axios.get(path);

      return response.data;
    },
    goToSettings() {
      this.$router.push({ name: 'settingsUser' });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
  },
};
</script>
