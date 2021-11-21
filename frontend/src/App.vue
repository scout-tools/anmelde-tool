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
  data: () => ({
    //
  }),
};
</script>
