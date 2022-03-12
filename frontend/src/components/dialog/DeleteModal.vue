<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Person löschen</v-card-title>

          <v-card-text> Diese Person komplett enfernen? </v-card-text>

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
      {{ 'Es ist ein  Fehler aufgetreten' }}
    </v-snackbar>
    <v-snackbar
      v-model="showSuccess"
      color="success"
      y="top"
      :timeout="timeout"
    >
      {{ 'Diese Person wurde erfolgreich gelöscht' }}
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
    data: {
      id: null,
    },
  }),

  methods: {
    onDeleteClick() {
      axios
        .delete(`${this.API_URL}basic/participant-personal/${this.data}/`)
        .then(() => {
          this.showSuccess = true;
          this.dialog = false;
          this.$emit('refresh');
        })
        .catch(() => {
          this.showError = true;
        });
    },
    show(item) {
      this.dialog = true;
      this.data = item;
    },

    cancel() {
      this.dialog = false;
    },
  },
};
</script>
