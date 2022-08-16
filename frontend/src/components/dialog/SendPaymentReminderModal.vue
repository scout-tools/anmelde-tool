<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Erringerungsmail senden?</v-card-title>

          <v-card-text>
            Bitte bestätige, dass du allen Anmeldungen mit negativer Zahlungsbilanz
            eine Erringerungsmail schicken willst.
          </v-card-text>

          <v-spacer/>
          <v-card-actions>
            <v-btn color="grey darken-1" text @click="cancel()">
              Abbrechen
            </v-btn>

            <v-btn color="green darken-1" text @click="onSendClick()">
              Senden
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <v-snackbar v-model="showError" color="error" y="top" :timeout="timeout">
      Es ist ein Fehler aufgetreten.
    </v-snackbar>
    <v-snackbar
        v-model="showSuccess"
        color="success"
        y="top"
        :timeout="timeout">
      Die Mails wurde erfolgreich versendet.
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
    eventId: null,
  }),

  methods: {
    onSendClick() {
      axios
        .post(`${this.API_URL}/event/cash/mail-reminder/`, {
          eventId: this.eventId,
        })
        .then(() => {
          this.showSuccess = true;
          this.dialog = false;
        })
        .catch((error) => {
          console.error(error);
          this.showError = true;
        });
    },
    open(eventId) {
      this.dialog = true;
      this.eventId = eventId;
    },
    cancel() {
      this.dialog = false;
    },
  },
};
</script>
