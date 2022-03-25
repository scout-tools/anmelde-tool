<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!isLoading">
            <v-card-title class="text-center justify-center py-6">
              Zu diesen Fahrten kannst du deinen Stamm anmelden
            </v-card-title>
            <v-list subheader two-line>
              <v-subheader inset>
                Nicht lange zögern. Melde deinen Stamm zu einer dieser Fahrten
                an.
              </v-subheader>
              <v-divider/>
              <template v-for="(item, index) in items">
                <v-list-item :key="item.name">
                  <v-list-item-avatar>

                    <v-icon
                      :class="'primary'"
                      dark
                      v-text="'mdi-tent'"
                    ></v-icon>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ getHeaderText(item) }}
                    </v-list-item-title>

                    <v-list-item-subtitle
                      v-text="item.description">
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getLagerText(item) }}
                    </v-list-item-subtitle>

                    <v-list-item-subtitle>
                      {{ getAnmeldephase(item) }}
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action v-show="item.canRegister && !getRegisteredId(item)">
                    <router-link
                      :to="{
                        name: 'registrationNew',
                        params: {
                          id: item.id,
                        },
                      }"
                      style="text-decoration: none"
                    >
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn icon v-bind="attrs" v-on="on">
                            <v-icon fab color="info">
                              mdi-account-multiple-plus
                            </v-icon>
                          </v-btn>
                        </template>
                        <span>Fahrtenanmeldung</span>
                      </v-tooltip>
                    </router-link>
                  </v-list-item-action>

                  <v-list-item-action
                    v-show="item.canEdit && getRegisteredId(item)"
                    class="ml-4"
                  >
                    <v-btn
                      icon
                      @click="editRegistration(getRegisteredId(item))"
                    >
                      <v-icon fab color="blue"> mdi-pencil </v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
                <v-divider
                  v-if="index < items.length - 1"
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
import moment from 'moment';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import ConfirmRegistrationEditModal from '@/views/registration/components/PreForm.vue';

export default {
  name: 'Main',
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    isLoading: true,
  }),
  components: {
    ConfirmRegistrationEditModal,
  },
  methods: {
    getLagerText(item) {
      const startDate = new Date(item.startDate);
      const endDate = new Date(item.endDate);
      return `Termin: ${moment(startDate, 'll', 'de')
        .format('ll')} bis
      ${moment(endDate, 'll', 'de')
    .format('ll')}`;
    },
    getAnmeldephase(item) {
      const registrationDeadline = new Date(item.registrationDeadline);
      const formatedRegistrationDeadline = moment(registrationDeadline, 'll', 'de').format('ll');

      const registrationStart = new Date(item.registrationStart);
      const formatedRegistrationStart = moment(registrationStart, 'll', 'de').format('ll');
      return `Anmeldephase ${formatedRegistrationStart} - ${formatedRegistrationDeadline}`;
    },
    getStartDate(item) {
      const registrationStart = new Date(item.registrationStart);
      return `Anmelde-Start: ${moment(registrationStart, 'll', 'de')
        .format('ll')}`;
    },
    getHeaderText(item) {
      if (item && item.registration.groupId) {
        return `${item.name} (Dein Stamm ist bereits Angemeldet)`;
      }
      if (item && item.registration.singleId) {
        return `${item.name} (Du bist bereits Angemeldet)`;
      }
      return item.name;
    },
    getRegisteredId(item) {
      if (!item.registration) {
        return null;
      }
      if (item.registration.groupId) {
        return item.registration.groupId;
      }
      if (item.registration.singleId) {
        return item.registration.singleId;
      }
      return null;
    },
    editRegistration(item) {
      this.$refs.confirmRegistrationEditModal.show(item);
    },
  },
  created() {
    this.isLoading = true;
    this.getEventOverview()
      .then((success) => {
        this.items = success.data;
        if (this.items.length === 0) {
          this.$router.push({ name: 'settingsUser' });
        }
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
};
</script>
