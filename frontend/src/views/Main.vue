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
    <router-view/>
  </v-app>
</template>

<script>
export default {
  name: 'Main',
};
</script>

<style scoped>

</style>
