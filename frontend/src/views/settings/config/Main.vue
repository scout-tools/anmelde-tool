<template>
  <v-card flat>
    <v-card-title class="text-center justify-center py-6">
      Hier kannst du deine Einstellungen anpassen.
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-subheader class="ma-5"> Wähle dein Farbschema aus. </v-subheader>
        <v-row>
          <v-col cols="12" sm="6">
            <v-select
              label="Farbschemen"
              :items="themeOptions"
              v-model="theme"
            />
          </v-col>
        </v-row>
          <v-row>
          <v-col cols="5">
            <v-autocomplete
              label="E-Mail Benachichtungen"
              :items="emailNotifactionList"
              v-model="data.emailNotifaction"
              @change="onEmailNotifactionChanged"
              item-value="value"
              item-text="name"
            />
          </v-col>
          <v-col cols="5">
            <v-autocomplete
              label="SMS Benachrichtungen"
              :items="smsOptionList"
              v-model="data.smsNotifcation"
              @change="onSmsNotificationChanged"
            />
          </v-col>
          </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from 'axios';
import serviceMixin from '@/mixins/serviceMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import { mapGetters } from 'vuex';

export default {
  mixins: [serviceMixin, apiCallsMixin],
  data() {
    return {
      data: {},
      personalData: {},
      emailNotifactionList: [],
      themeOptions: [
        {
          text: 'Normal',
          value: 'default',
        },
        {
          text: 'DPV-Gold',
          value: 'dpvgold',
        },
        {
          text: 'DPBM',
          value: 'mosaik',
        },
        {
          text: 'Winkinger',
          value: 'wikinger',
        },
        {
          text: 'Silberfüchse',
          value: 'silberfuechse',
        },
      ],
      smsOptionList: [
        {
          text: 'Ja',
          value: true,
        },
        {
          text: 'Nein',
          value: false,
        },
      ],
    };
  },
  computed: {
    ...mapGetters(['userinfo']),
    theme: {
      get() {
        return this.$store.state.preferences.theme;
      },
      set(theme) {
        this.$store.commit('setTheme', theme);
      },
    },
  },
  methods: {
    convertEnum(list) {
      return list.map((x) => { // eslint-disable-line
        return {
          value: x[0],
          name: x[1],
        };
      });
    },
    onEmailNotifactionChanged() {
      this.loading = true;
      const path = `${this.API_URL}/auth/email-settings/${this.personalData.id}/`;
      axios
        .patch(path, {
          emailNotifaction: this.data.emailNotifaction,
        })
        .then(() => {
          this.$root.globalSnackbar.show({
            message: 'Gespeichert',
            color: 'success',
          });
          this.loading = false;
        });
    },
    onSmsNotificationChanged() {
      this.loading = true;
      const path = `${this.API_URL}/auth/email-settings/${this.personalData.id}/`;
      axios
        .patch(path, {
          smsNotifcation: this.data.smsNotifcation,
        })
        .then(() => {
          this.$root.globalSnackbar.show({
            message: 'Gespeichert',
            color: 'success',
          });
          this.loading = false;
        });
    },
    saveEmailSettings() {
      this.loading = true;
      const path = `${this.API_URL}/auth/email-settings/`;
      axios
        .post(path, {
          scoutOrganisation: this.scoutOrganisation.id,
        })
        .then(() => {
          this.$root.globalSnackbar.show({
            message: 'Neuer Eintrag angelegt',
            color: 'success',
          });
          this.loading = false;
        });
    },
    loadData() {
      Promise.all([
        this.getPersonalData(),
        this.getSimpleService('/auth/email-notification-types/'),
      ]).then((values) => {
        this.personalData = values[0].data;
        this.getSimpleService(`/auth/email-settings/${values[0].data.id}/`).then((response) => {
          this.data = response.data;
        });
        this.emailNotifactionList = this.convertEnum(values[1].data);
      });
    },
  },
  created() {
    this.loadData();
  },
};
</script>

<style>
</style>
