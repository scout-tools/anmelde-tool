<template>
  <v-app>
    <div id="app">
      <main-comp/>
    </div>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

import MainComp from './views/Main.vue';

export default {
  name: 'App',

  components: {
    MainComp,
  },
  created() {
    document.title = 'Anmelde-Tool für Pfadfinder_innen';
    this.setThemeByQuery();
  },
  methods: {
    setThemeByQuery() {
      if (this.$route.query.theme) {
        this.$store.commit('setTheme', this.$route.query.theme);
      }
      this.$store.commit('setTheme', this.theme);
    },
  },
  computed: {
    ...mapGetters(['theme']),
  },
  data: () => ({
    //
  }),
};
</script>

<style>
.top-margin {
  margin-top: 70px !important;
}
.default-max-width {
  max-width: 800px !important;
}
</style>
