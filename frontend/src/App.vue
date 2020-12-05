<template>
  <v-app>
    <div id="app">
      <main-comp class="mt-100p"/>
    </div>
  </v-app>
</template>

<script>
import MainComp from './views/Main.vue';

export default {
  name: 'App',

  components: {
    MainComp,
  },

  data: () => ({
    //
  }),
};
</script>

<style>
  .mt-100p {
    margin-top: 100px;
  }
</style>
