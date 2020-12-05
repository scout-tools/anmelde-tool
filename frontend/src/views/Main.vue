<template>
  <v-app>
    <v-app-bar
      app
      color="#1a4b7e"
      dark
    >
      <span>Menu</span>
      <v-spacer/>
      <v-btn outlined dark to="/login">
        Login
      </v-btn>
    </v-app-bar>
    <overview-card/>
    <router-view/>
  </v-app>
</template>

<script>
import OverviewCard from './overview/Overview.vue';

export default {
  name: 'Main',
  components: {
    OverviewCard,
  },
};
</script>

<style scoped>

</style>
