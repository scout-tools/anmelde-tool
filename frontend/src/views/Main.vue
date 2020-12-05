<template>
  <v-app>
    <v-app-bar
      app
      color="#1a4b7e"
      dark
    >
      <span>Menu</span>
      <v-spacer/>
      <v-btn
        class="mx-2"
        fab
        dark
        color="indigo"
      >
        <v-icon dark>
          mdi-plus
        </v-icon>
      </v-btn>
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
