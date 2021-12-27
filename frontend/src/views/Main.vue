<template>
  <v-app>
    <top-menu-main/>
    <router-view/>
    <gobal-snackbar ref="globalSnackbar"/>
    <footer-main class="mt-auto"/>
  </v-app>
</template>

<script>
import TopMenuMain from '@/components/TopMenu.vue';
import FooterMain from '@/components/Footer.vue';
import GobalSnackbar from '@/components/modals/GlobalSnackbar.vue';

export default {
  name: 'Main',
  components: {
    TopMenuMain,
    FooterMain,
    GobalSnackbar,
  },
  mounted() {
    this.$root.globalSnackbar = this.$refs.globalSnackbar;
  },
};
</script>
