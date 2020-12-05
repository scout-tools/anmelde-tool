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

  data: () => ({
    //
  }),
};
</script>
