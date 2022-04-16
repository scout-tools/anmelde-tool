<template>
  <v-container class="top-margin">
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card v-if="!loading">
            <v-card-title class="text-center justify-center py-6">
              Zu diesen Fahrten kannst du deinen Stamm oder dich anmelden
            </v-card-title>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    loading: false,
    data: {},
  }),
};
</script>

<style>
</style>
