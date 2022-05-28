<template>
  <v-card flat class="ma-5">
    <v-data-table
      :headers="headers"
      :items="items"
      hide-default-footer
      show-expand
      single-expand
      :expanded.sync="expanded"
    >
      <template v-slot:top>
        <v-container fluid>
          <v-row justify="start" align="center">
            <v-col cols="4">
              <v-text-field
                label="Suche"
                dense
                v-model="filter.search"
                prepend-inner-icon="mdi-magnify"
                @input="onFilterSelected"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-select
                label="Typ"
                prepend-inner-icon=""
                v-model="filter.messageTypes"
                :items="messageTypes"
                dense
                item-value="id"
                multiple
                item-text="name"
                @change="onFilterSelected"
              >
                <template v-slot:selection="{ item, index }">
                  <template v-if="index === 0">
                    <span>{{ item.name }}</span>
                  </template>
                  <span v-if="index === 1" class="grey--text text-caption">
                    + {{ filter.messageTypes.length - 1 }}
                  </span>
                </template>
              </v-select>
            </v-col>
            <v-col cols="4">
              <v-checkbox
                v-model="filter.isProcessed"
                label="Noch Offen"
                @change="onFilterSelected"
              ></v-checkbox>
            </v-col>
          </v-row>
        </v-container>
      </template>
      <template v-slot:[`item.isProcessed`]="{ item }">
        <v-icon :color="item.isProcessed ? 'green' : 'red'">
          {{ item.isProcessed ? 'mdi-check-circle' : 'mdi-close-circle' }}
        </v-icon>
      </template>
      <template v-slot:[`item.createdAt`]="{ item }">
        {{ formatDate(item.createdAt) }}
      </template>
      <template v-slot:[`item.messageType`]="{ item }">
        {{ getName(item.messageType) }}
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <v-container fluid>
            <v-row class="ma-3">
              <v-textarea label="Nachricht" readonly v-model="item.messageBody">
              </v-textarea>
            </v-row>
            <v-row class="ma-3">
              <v-textarea
                label="Interner Vermerk"
                readonly
                v-model="item.internalComment"
              >
              </v-textarea>
            </v-row>
            <v-row class="ma-3">
              <v-btn
                @click="openProceedDialog(item)"
                :color="!item.isProcessed ? 'success' : 'error'"
                >{{
                  !item.isProcessed ? 'Erledigt' : 'Doch nicht erledigt'
                }}</v-btn
              >
            </v-row>
          </v-container>
        </td>
      </template>
    </v-data-table>
    <MessageProsessedDialog
      ref="messageProsessedDialogRef"
      @refresh="onFilterSelected"
    />
  </v-card>
</template>

<script>
import serviceMixin from '@/mixins/serviceMixin';
import moment from 'moment'; // eslint-disable-line

import MessageProsessedDialog from './MessageProsessedDialog.vue';

export default {
  mixins: [serviceMixin],
  components: {
    MessageProsessedDialog,
  },
  data: () => ({
    items: [],
    messageTypes: [],
    loading: true,
    filter: {
      isProcessed: true,
    },
    expanded: [],
    headers: [
      {
        text: 'Erledigt?',
        value: 'isProcessed',
      },
      {
        text: 'Erstellt',
        value: 'createdAt',
      },
      {
        text: 'Typ',
        value: 'messageType',
      },
      {
        text: 'Ersteller',
        value: 'createdByEmail',
      },
      {
        text: 'Bearbeiter',
        value: 'supervisor',
      },
      {
        text: '',
        value: 'data-table-expand',
      },
    ],
  }),
  methods: {
    openProceedDialog(item) {
      this.$refs.messageProsessedDialogRef.open(item);
    },
    getName(value) {
      return this.messageTypes.filter((item) => item.id === value)[0].name;
    },
    formatDate(item) {
      return moment(item).format('DD.MM.YYYY');
    },
    getData(params) {
      this.loading = true;
      Promise.all([
        this.getSimpleService('/basic/message/', params),
        this.getSimpleService('/basic/message-type/'),
      ])
        .then((values) => {
          this.items = values[0].data;
          this.messageTypes = values[1].data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Leider ist ein Problem beim runterladen des Events aufgetreten, bitte probiere es später nocheinmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onFilterSelected() {
      const params = new URLSearchParams();
      if (this.filter.messageTypes) {
        this.filter.messageTypes.forEach((value) => {
          params.append('message_type', value);
        });
      }

      if (this.filter.search) {
        params.append('search', this.filter.search);
      }

      if (this.filter.isProcessed) {
        params.append('is_processed', !this.filter.isProcessed);
      }
      this.getData(params);
    },
  },
  created() {
    this.onFilterSelected();
  },
};
</script>

<style>
</style>
