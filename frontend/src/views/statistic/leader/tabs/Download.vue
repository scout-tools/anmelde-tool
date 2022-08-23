<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0">
            <v-row class="center text-center justify-center pa-0">
              <v-col cols="6">
                <v-autocomplete
                    clearable
                    :loading="loading"
                    :items="availableFileTemplates"
                    v-model="selectedFileTemplateFilter"
                    label="Filter nach Typ"
                    multiple
                    item-text="type"
                    item-value="id"
                    @change="onFilterSelected"
                    no-data-text="Keine Datei Typen gefunden."
                />
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                    clearable
                    :loading="loading"
                    :items="availableStatus"
                    v-model="selectedStatusFilter"
                    label="Filter nach Status"
                    multiple
                    item-text="name"
                    item-value="value"
                    @change="onFilterSelected"
                />
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
                    :loading="loading"
                    no-data-text="Keine Downloads verfügbar.">
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
            Fehlermeldung:
            <pre> {{ item.errorMsg }} </pre>
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
    availableFileTemplates: [],
    selectedFileTemplateFilter: [],
    selectedStatusFilter: [],
    currentSearchParams: null,
    expanded: [],
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
        value: 'template.type',
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
    itemsPerPage: 10,
    loading: false,
    availableStatus: [
      {
        name: 'In der Warteschlange',
        value: 'Q',
        color: 'grey',
      },
      {
        name: 'Wird generiert',
        value: 'P',
        color: 'blue',
      },
      {
        name: 'Erfolgreich',
        value: 'FS',
        color: 'green',
      },
      {
        name: 'Fehlgeschlagen',
        value: 'FF',
        color: 'red',
      },
    ],
    interval: null,
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
      return this.availableStatus.find((x) => x.value === status).color;
    },
    getStatusText(status) {
      return this.availableStatus.find((x) => x.value === status).name;
    },
    getUserText(user) {
      if (!user) return '';
      return `${user.userextended.scoutName} (${user.userextended.scoutOrganisation.name})`;
    },
    formatDate(item) {
      return moment(item)
        .locale('de')
        .format('lll');
    },
    getData(params) {
      this.loading = true;

      Promise.all([
        this.getDownloadSummary(this.eventId, params),
        this.getAvailableFileTemplates(),
      ])
        .then((values) => {
            this.data = values[0].data; //eslint-disable-line
            this.availableFileTemplates = values[1].data; //eslint-disable-line
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onRefresh() {
      this.getData();
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
    onFilterSelected() {
      const params = new URLSearchParams();
      if (this.selectedFileTemplateFilter) {
        this.selectedFileTemplateFilter.forEach((value) => {
          params.append('file-type', value);
        });
      }
      if (this.selectedStatusFilter) {
        this.selectedStatusFilter.forEach((value) => {
          params.append('status', value);
        });
      }
      this.getData(params);
      this.currentSearchParams = params;
    },
  },
  created() {
    this.getData(this.currentSearchParams);
    this.interval = window.setInterval(() => {
      this.getData(this.currentSearchParams);
    }, 30000);
  },
  destroyed() {
    clearInterval(this.interval);
  },
};

</script>
