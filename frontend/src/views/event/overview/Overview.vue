<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!loading">
            <v-card-title class="text-center justify-center py-6">
              Zu diesen Fahrten kannst du deinen Stamm oder dich anmelden
            </v-card-title>
            <v-list subheader two-line>
              <p
                class="text-center"
                v-if="isDev"
                style="border-style: solid; border-color: red"
              >
                <v-icon color="red darken-1" large class="ma-2">
                  mdi-alert mdi-spin
                </v-icon>
                Dies ist ein Test-Server. Die Anmeldung sind
                <b>nicht verbindlich</b> und werden regelmäßig gelöscht.
                <v-icon color="red darken-1" large class="ma-2">
                  mdi-alert mdi-flip-h mdi-spin
                </v-icon>
                <br />
                <br />
                Immer wenn das Logo <b>oben links rot </b> ist befindest du dich
                auch dem Test-Server.
              </p>
              <v-subheader inset>
                Folgende Fahrten stehen dir aktuell für die Anmeldung zur
                Auswahl. Klicke einfach auf eine Fahrt um mehr zu erfahren.
              </v-subheader>
              <v-divider />
              <v-list-group
                v-for="(item, index) in items"
                :key="item.name"
                :prepend-icon="item.action"
                no-action>
                <template v-slot:activator>
                  <v-list-item-avatar>
                    <v-icon
                      large
                      color="primary"
                      dark>
                      {{ `mdi-${item.icon || 'tent'}` }}
                    </v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ getHeaderText(item) }}
                      <v-icon v-if="item.isConfirmed === false" color="red">
                        mdi-close-octagon
                      </v-icon>
                      <v-icon v-if="item.isConfirmed === true" color="green">
                        mdi-check
                      </v-icon>
                    </v-list-item-title>

                    <v-list-item-subtitle>
                      {{ item.shortDescription }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getLagerText(item) }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getAnmeldephase(item) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>
                </template>
                <v-list-item>
                  <v-container>
                    <v-row class="pa-2">
                      <td v-html="item.longDescription"></td>
                    </v-row>
                    <v-row>
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-bind="attrs"
                            v-on="on"
                            class="ma-3"
                            @click="onSingleRegClicked(item)"
                            v-if="item.registrationOptions.allowNewSingleReg"
                          >
                            <v-icon fab color="success">
                              mdi-account-plus
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Einzel Fahrtenanmeldung</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-bind="attrs"
                            v-on="on"
                            class="ma-3"
                            @click="onGroupRegClicked(item)"
                            v-if="item.registrationOptions.allowNewGroupReg"
                          >
                            <v-icon fab color="success">
                              mdi-account-multiple-plus
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Gruppen Fahrtenanmeldung</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="item.registrationOptions.allowEditSingleReg"
                            :disabled="
                              !item.registrationOptions.allowEditSingleReg
                            "
                            class="ma-3"
                            @click="editRegistration(item, true)"
                            v-bind="attrs"
                            v-on="on"
                          >
                            <v-icon fab color="blue"> mdi-pencil </v-icon>
                          </v-btn>
                        </template>
                        <span>Einzelanmeldung bearbeiten</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="item.registrationOptions.allowEditGroupReg"
                            class="ma-3"
                            @click="editRegistration(item, false)"
                            v-bind="attrs"
                            v-on="on"
                          >
                            <v-icon fab color="blue"> mdi-pencil </v-icon>
                          </v-btn>
                        </template>
                        <span>Gruppenanmeldung bearbeiten</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="
                              item.registrationOptions.allowEditGroupReg || // eslint-disable-line
                              item.registrationOptions.allowEditSingleReg
                            "
                            class="ma-3"
                            @click="onAddResponsablePerson(item)"
                            v-bind="attrs"
                            v-on="on"
                          >
                            <v-icon fab color="success">
                              mdi-share-variant
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Weitere Person Freigeben</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="item.registrationOptions.allowEditSingleReg"
                            class="ma-3"
                            @click="deleteRegistration(getRegisteredId(item, true))"
                            v-bind="attrs"
                            v-on="on">
                            <v-icon fab color="red"> mdi-close </v-icon>
                          </v-btn>
                        </template>
                        <span>Einzelanmeldung Abmelden</span>
                      </v-tooltip>

                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            v-if="item.registrationOptions.allowEditGroupReg"
                            class="ma-3"
                            @click="deleteRegistration(getRegisteredId(item, false))"
                            v-bind="attrs"
                            v-on="on">
                            <v-icon fab color="red"> mdi-close </v-icon>
                          </v-btn>
                        </template>
                        <span>Gruppenanmeldung Abmelden</span>
                      </v-tooltip>

                      <!-- <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            class="ma-3"
                            @click="sendMessage(getRegisteredId(item))"
                            v-bind="attrs"
                            v-on="on"
                          >
                            <v-icon fab color="primary">
                              mdi-chat-question
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Frage an die Lagerleitung</span>
                      </v-tooltip> -->

                      <router-link
                        :to="{
                          name: 'statisticOverview',
                          params: { id: item.id },
                        }"
                        class="ma-3"
                        style="text-decoration: none">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn
                              v-bind="attrs"
                              v-on="on"
                              v-if="item.allowStatistic">
                              <v-icon color="primary"> mdi-chart-bar </v-icon>
                            </v-btn>
                          </template>
                          <span>Fahrtenstatistik</span>
                        </v-tooltip>
                      </router-link>
                      <router-link
                        :to="{
                          name: 'statisticOverview',
                          params: { id: item.id },
                        }"
                        class="ma-3"
                        style="text-decoration: none">
                        <v-tooltip bottom>
                          <template v-slot:activator="{ on, attrs }">
                            <v-btn
                              v-bind="attrs"
                              v-on="on"
                              v-if="!item.allowStatistic && item.allowStatisticLeader">
                              <v-icon color="primary"> mdi-chart-bar </v-icon>
                            </v-btn>
                          </template>
                          <span>Fahrtenstatistik für Bundesführende</span>
                        </v-tooltip>
                      </router-link>
                    </v-row>
                  </v-container>
                </v-list-item>
                <v-divider
                  v-if="index < items.length - 1"
                  :key="index"
                ></v-divider>
              </v-list-group>
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
    <DeleteModal ref="deleteModal" />
    <SendMessageModal ref="sendMessageModal" />
    <EventCodeModal ref="eventCodeModal" />
    <DialogAddResponsablePerson ref="dialogAddResponsablePerson" />
  </v-container>
</template>

<script>
import moment from 'moment';
import { mapGetters } from 'vuex';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import ConfirmRegistrationEditModal from '@/views/registration/components/PreForm.vue';
import DeleteModal from '@/views/registration/components/DeleteModal.vue';
import SendMessageModal from '@/views/registration/components/SendMessageModal.vue';
import EventCodeModal from '@/views/event/components/EventCodeModal.vue';
import DialogAddResponsablePerson from '@/components/dialog/DialogAddResponsablePerson.vue';

export default {
  name: 'OverviewMain',
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    loading: true,
  }),
  components: {
    ConfirmRegistrationEditModal,
    DeleteModal,
    SendMessageModal,
    EventCodeModal,
    DialogAddResponsablePerson,
  },
  computed: {
    ...mapGetters(['theme']),
    isDev() {
      return process.env.VUE_APP_ENV === 'DEV';
    },
  },
  methods: {
    getLagerText(item) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);
      return `Termin: ${moment(startDate, 'll', 'de').format('ll')} bis
      ${moment(endDate, 'll', 'de').format('ll')}`;
    },
    getAnmeldephase(item) {
      const registrationDeadline = new Date(item.registrationDeadline);
      const formatedRegistrationDeadline = moment(
        registrationDeadline,
        'll',
        'de',
      ).format('ll');

      const registrationStart = new Date(item.registrationStart);
      const formatedRegistrationStart = moment(
        registrationStart,
        'll',
        'de',
      ).format('ll');
      if (registrationDeadline < new Date()) {
        return `Der Anmeldeschluss ist seit dem ${formatedRegistrationDeadline} vorbei.`;
      }
      if (formatedRegistrationStart > new Date()) {
        return `Der Anmeldestart beginnt am ${formatedRegistrationStart}.`;
      }
      return `Anmeldephase ${formatedRegistrationStart} - ${formatedRegistrationDeadline}`;
    },
    getStartDate(item) {
      const registrationStart = new Date(item.registrationStart);
      return `Anmelde-Start: ${moment(registrationStart, 'll', 'de').format(
        'll',
      )}`;
    },
    getHeaderText(item) {
      if (item && item.registrationOptions.groupId && item.isConfirmed) {
        return `${item.name} (Dein Stamm ist bereits Angemeldet)`;
      }
      if (item && item.registrationOptions.groupId && !item.isConfirmed) {
        return `${item.name} (Deine Stammesanmeldung ist nicht abgeschlossen)`;
      }
      if (item && item.registrationOptions.singleId && item.isConfirmed) {
        return `${item.name} (Du bist bereits Angemeldet)`;
      }
      if (item && item.registrationOptions.singleId && !item.isConfirmed) {
        return `${item.name} (Deine Anmeldung ist nicht angeschlossen)`;
      }
      return item.name;
    },
    getRegisteredId(item, single = false) {
      if (!item.registrationOptions) {
        return null;
      }
      if (item.registrationOptions.groupId && !single) {
        return item.registrationOptions.groupId;
      }
      if (item.registrationOptions.singleId) {
        return item.registrationOptions.singleId;
      }
      return null;
    },
    editRegistration(item, single) {
      this.setTheme(item.theme);
      this.$refs.confirmRegistrationEditModal.show(
        this.getRegisteredId(item, single),
      );
    },
    onSingleRegClicked(item) {
      this.openEventCodeModal(item, true, item.singleRegistrationLevel);
    },
    onGroupRegClicked(item) {
      this.openEventCodeModal(item, false, item.groupRegistrationLevel);
    },
    openEventCodeModal(item, single, registrationLevel) {
      this.setTheme(item.theme);
      this.$refs.eventCodeModal.show(item, single, registrationLevel);
    },
    onAddResponsablePerson(item) {
      this.$refs.dialogAddResponsablePerson.open(item);
    },
    deleteRegistration(item) {
      this.$refs.deleteModal.show(item);
    },
    sendMessage(item) {
      this.$refs.sendMessageModal.show(item);
    },
    setTheme(id) {
      this.getServiceById('basic/theme', id).then((response) => {
        this.$store.commit('setTheme', response.data.name);
      });
    },
  },
  created() {
    this.loading = true;
    this.getEventOverview()
      .then((success) => {
        this.items = success.data;
        if (this.items.length === 0) {
          this.$router.push({ name: 'settingsUser' });
        } else {
          this.$store.commit('setAccountIncomplete', false);
        }
      })
      .catch(() => {
        this.$root.globalSnackbar.show({
          message:
            'Leider ist ein Problem beim anzeigen der Events aufgetreten, bitte probiere es später nocheinmal.',
          color: 'error',
        });
      })
      .finally(() => {
        this.loading = false;
      });
  },
};
</script>
