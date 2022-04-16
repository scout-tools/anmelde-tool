<template>
  <v-app>
    <top-menu-main v-if="!isMobile" />
    <router-view v-if="!isMobile" />
    <v-container fluid v-else>
      <v-row align="center" justify="center" class="ma-10">
        Die Smartphone Version befindet sich noch in der Testphase.
        Bitte wechsel zu einem größeren Bildschirm oder maximiere das Fenster.
      </v-row>
      <v-row align="center" justify="center" class="ma-10">
        <v-icon large color="error">mdi-cellphone-off</v-icon>
      </v-row>
    </v-container>
    <gobal-snackbar ref="globalSnackbar" />
    <footer-main class="mt-auto" />
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
  computed: {
    isMobile() {
      return this.$vuetify.breakpoint.smAndDown;
    },
  },
  mounted() {
    this.$root.globalSnackbar = this.$refs.globalSnackbar;
  },
};
</script>
