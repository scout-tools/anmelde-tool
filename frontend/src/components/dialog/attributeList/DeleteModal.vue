<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Löschen</v-card-title>

          <v-card-text> enfernen? </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="grey darken-1" text @click="cancel()">
              Behalten
            </v-btn>

            <v-btn color="red darken-1" text @click="onDeleteClick()">
              Löschen
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
      {{ 'Es ist ein Fehler aufgetreten' }}
    </v-snackbar>
    <v-snackbar
      v-model="showSuccess"
      color="success"
      y="top"
      :timeout="timeout"
    >
      {{ 'Dieser Eintrag wurde erfolgreich gelöscht' }}
    </v-snackbar>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    showError: false,
    showSuccess: false,
    timeout: 3000,
    id: null,
  }),
  props: {
    dialogMeta: {
      default: {},
    },
    valdiationObj: {
      default: {},
    },
    moduleMapper: {
      default: {},
    },
  },
  computed: {
    path() {
      return `${this.API_URL}/event/event/${this.dialogMeta.regId}/event-module-mapper/${this.moduleMapper.id}/attribute-mapper/`;
    },
    attributeMapperId() {
      return this.id;
    },
  },
  methods: {
    onDeleteClick() {
      axios
        .delete(`${this.path}${this.attributeMapperId}/`)
        .then(() => {
          this.showSuccess = true;
          this.dialog = false;
          this.$emit('refresh');
        })
        .catch(() => {
          this.showError = true;
        });
    },
    show(id) {
      this.dialog = true;
      this.id = id;
    },

    cancel() {
      this.dialog = false;
    },
  },
};
</script>
