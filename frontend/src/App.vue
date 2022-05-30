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

};
</script>

<style lang="sass">
@import '../node_modules/typeface-roboto/index.css'
</style>
<style>
.top-margin {
  margin-top: 80px !important;
  margin-bottom: 80px !important;
}
.default-max-width {
  width: 800px !important;
}
</style>
