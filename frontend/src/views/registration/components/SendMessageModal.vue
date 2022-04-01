<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Nachricht senden</v-card-title>
          <v-card-text>
            Nachricht an die Lagerleitung senden.
            <v-textarea       solo
      auto-grow>
            </v-textarea>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="grey darken-1" text @click="cancel()"> Zurück </v-btn>
            <v-btn color="success" text @click="onDeleteClicked"> Senden </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    showError: false,
    showSuccess: false,
    timeout: 3000,
    id: null,
  }),
  mixins: [apiCallsMixin],
  methods: {
    onDeleteClicked() {
      this.dialog = false;
    },
    show(item) {
      this.dialog = true;
      this.id = item;
    },

    cancel() {
      this.dialog = false;
    },
  },
};
</script>
