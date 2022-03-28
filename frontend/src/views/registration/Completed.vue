<template>
  <v-container fluid class="ma-10">
    <v-card class="mx-auto top-margin default-max-width">
      <v-row align="center" justify="center" class="ma-10">
        Danke für die Registrierung.
      </v-row>
      <v-row align="center" justify="center" class="ma-10">
        Du hast eine Zusammenfassung per Mail erhalten.
      </v-row>
      <v-row align="center" justify="center" class="ma-10">
        <v-btn
          class="ma-10"
          color="success"
          x-large
          @click="$router.push({ name: 'eventOverview' })"
        >
          <v-icon left>mdi-rocket-launch</v-icon>
          Zurück zur Übersicht
        </v-btn>
      </v-row>
    </v-card>
  </v-container>
</template>

<script>
export default {};
</script>

<style>
</style>
