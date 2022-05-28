<template>
  <v-expand-transition>
    <v-container fluid class="ma-0 pa-0">
      <v-row>
        <v-col :cols="selectedItem.length ? '7' : '12'">
          <v-data-table
            v-model="selectedItem"
            :headers="headers"
            :items="items"
            hide-default-footer
            single-expand
            single-select
            show-select
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
                        <span
                          v-if="index === 1"
                          class="grey--text text-caption"
                        >
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
          </v-data-table>
          <MessageProsessedDialog
            ref="messageProsessedDialogRef"
            @refresh="onFilterSelected"
          />
        </v-col>
        <v-col
          style="background:#f5f5f5;"
          :cols="selectedItem.length ? '5' : '0'"
          v-show="selectedItem.length"
        >
          <v-container fluid>
            <v-row class="ma-3">
              <v-btn
              class="ma-2"
                @click="openProceedDialog(selectedItem[0])"
                color="primary"
                ><v-icon>
                  mdi-tools
                  </v-icon>
                </v-btn>
              <v-btn
              class="ma-2"
                @click="deleteItem(selectedItem[0])"
                color="error"
                ><v-icon>
                  mdi-delete
                  </v-icon>
                </v-btn>
                <v-spacer></v-spacer>
              <v-btn
                icon
              class="ma-2"
                @click="selectedItem = []"
                ><v-icon>
                  mdi-window-close
                  </v-icon>
                </v-btn>
            </v-row>
            <v-row class="ma-1">
              <v-text-field
                label="Typ"
                readonly
                v-model="item.messageType"
              >
              </v-text-field>
            </v-row>
            <v-row class="ma-1">
              <v-textarea
                label="Nachricht"
                readonly
                v-model="item.messageBody"
              >
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
          </v-container>
        </v-col>
      </v-row>
    </v-container>
  </v-expand-transition>
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
    selectedItem: [],
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
      // {
      //   text: 'Typ',
      //   value: 'messageType',
      // },
      {
        text: 'Ersteller',
        value: 'createdByEmail',
      },
      {
        text: 'Bearbeiter',
        value: 'supervisor',
      },
      // {
      //   text: '',
      //   value: 'data-table-expand',
      // },
    ],
  }),
  computed: {
    item() {
      if (this.selectedItem && this.selectedItem.length) {
        return this.selectedItem[0];
      }
      return {
        messageBody: '',
      };
    },
  },
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
