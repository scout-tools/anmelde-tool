<template>
  <div>
    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Registrierung ändern</v-card-title>

          <v-card-text>
            Wollen Sie die Registrierung wirklich ändern?<br />
            Dies bedeutet, dass sie automatisch <b>abgemeldet</b> werden und
            sich wieder selber anmelden müssen.
          </v-card-text>

          <v-card-actions>
            <v-spacer/>

            <v-btn color="grey darken-1" text @click="cancel()">
              Zurück
            </v-btn>
            <v-btn
              color="grey darken-1"
              text
              :to="{
                name: 'registrationEdit',
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
