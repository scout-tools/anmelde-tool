<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Registrierung ändern</v-card-title>

          <v-card-text> Wollen Sie die Registrierung wirklich änder?<br>
          Dies bedeutet, dass sie automatisch <b>abgemeldet</b> werden und sich wieder selber
          anmelden müssen.</v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="grey darken-1" text @click="cancel()">
              Zurück
            </v-btn>
            <v-btn color="grey darken-1" text :to="{
                name: 'registrationCreate',
                params: { id: id },
              }">
              Ändern
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
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

  methods: {
    onEditClick() {
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
