<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0">
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="6">
                <v-checkbox
                  v-model="filter.justConfirmed"
                  label="Nur Bestätigt"
                  hide-details/>
              </v-col>
              <v-col cols="6">
                <v-btn
                  @click="onNewClicked()"
                  color="primary"
                  dark>
                  Neue Datei anfordern
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">
      <v-data-table :headers="headers"
                    :items="getItems"
                    :items-per-page="itemsPerPage"
                    :expanded.sync="expanded"
                    show-expand
                    single-expand
                    hide-default-footer
                    item-key="createdAt"
                    :loading="loading">
        <template v-slot:[`item.createdAt`]="{ item }">
          {{ formatDate(item.createdAt) }}
        </template>
        <template v-slot:[`item.updatedAt`]="{ item }">
          {{ formatDate(item.updatedAt) }}
        </template>
        <template v-slot:[`item.status`]="{ item }">
          <v-chip :color="getColor(item.status)" dark>
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>
        <template v-slot:[`item.user`]="{ item }">
          {{ getUserText(item.user) }}
        </template>
        <template v-slot:[`item.file`]="{ item }">
          <v-btn
            :disabled="!item.file"
            @click="onDownloadClicked(item.file)"
            color="primary"
            small
            icon
            dark>
            <v-icon dark>
              mdi-download
            </v-icon>
          </v-btn>
        </template>
        <template v-slot:expanded-item="{ item }">
          <td :colspan="headers.length">
            Fehlermeldung: {{ item.errorMsg }}
          </td>
        </template>
      </v-data-table>
    </v-row>
    <GenerateFileRequestModal
      ref="requestFileModal"
      @createFileRequest="createFileRequest"/>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import moment from 'moment'; // eslint-disable-line
import GenerateFileRequestModal from '@/components/dialog/GenerateFileRequestModal.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    GenerateFileRequestModal,
  },
  data: () => ({
    data: [],
    expanded: [],
    filter: {
      justConfirmed: true,
    },
    headers: [
      {
        text: 'Angefordert um',
        value: 'createdAt',
      },
      {
        text: 'Zuletzt geupdadet',
        value: 'updatedAt',
      },
      {
        text: 'Typ',
        value: 'type',
      },
      {
        text: 'Format',
        value: 'extension',
      },
      {
        text: 'Status',
        value: 'status',
      },
      {
        text: 'Angefordert von',
        value: 'user',
      },
      {
        text: 'Datei',
        value: 'file',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
    dialog: false,
    API_URL: process.env.VUE_APP_API,
    showError: false,
    responseObj: null,
    itemsPerPage: 1000,
    loading: false,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getItems() {
      if (!this.data) return [];
      return this.data;
    },
  },
  methods: {
    getColor(status) {
      if (status === 'Q') return 'grey';
      if (status === 'P') return 'blue';
      if (status === 'FS') return 'green';
      if (status === 'FF') return 'red';
      return 'green';
    },
    getStatusText(status) {
      if (status === 'Q') return 'In der Warteschlange';
      if (status === 'P') return 'Wird generiert';
      if (status === 'FS') return 'Erfolgreich';
      if (status === 'FF') return 'Fehlgeschlagen';
      return 'green';
    },
    getUserText(user) {
      if (!user) return '';
      return `${user.userextended.scoutName} (${user.userextended.scoutOrganisation.name})`;
    },
    formatDate(item) {
      return moment(item)
        .locale('de')
        .format('LLL');
    },
    getData(eventId) {
      this.loading = true;
      this.getDownloadSummary(eventId)
        .then((responseObj) => {
          this.data = responseObj.data; // eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onRefresh() {
      this.getData(this.eventId);
    },
    onNewClicked() {
      this.$refs.requestFileModal.open();
    },
    createFileRequest(data) {
      this.addFileRequest(this.eventId, data)
        .then(() => {
          this.onRefresh();
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim erstellen der Datei Anforderung aufgetreten,'
              + ' bitte probiere es später nocheinmal.',
            color: 'error',
            timer: 5000,
          });
        });
    },
    onDownloadClicked(url) {
      window.open(url);
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
