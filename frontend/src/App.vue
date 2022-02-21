<template>
  <v-app>
    <div id="app">
      <main-comp/>
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
  created() {
    document.title = 'Anmelde-Tool für Pfadfinder_innen';
  },

};
</script>

<style lang="sass">
@import '../node_modules/typeface-roboto/index.css'
</style>
