<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Überweisung löschen</v-card-title>

          <v-card-text>
            Diesen Überweisungsbeleg vom {{ formatDate(data.transferDate) }} mit dem Betreff
            {{ data.transferSubject }} über {{ getPrice(data.amount) }} komplett enfernen?
          </v-card-text>

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
      :timeout="timeout">
      {{ 'Diesen Überweisungsbeleg wurde erfolgreich gelöscht' }}
    </v-snackbar>
  </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

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
        .delete(`${this.API_URL}/event/cash/income/${this.data.id}/`)
        .then(() => {
          this.showSuccess = true;
          this.dialog = false;
          this.$emit('refresh');
        })
        .catch((error) => {
          console.error(error);
          this.showError = true;
        });
    },
    open(item) {
      this.dialog = true;
      this.data = item;
    },
    cancel() {
      this.dialog = false;
    },
    formatDate(item) {
      return moment(item)
        .format('DD.MM.YYYY');
    },
    getPrice(item) {
      return item ? `${item} €` : '0 €';
    },
  },
};
</script>
