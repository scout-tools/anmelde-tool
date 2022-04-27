<template>
  <v-app>
    <top-menu-main v-if="!isMobile" />
    <router-view class="mb-12" v-if="!isMobile" />
    <v-container fluid v-else>
      <v-row align="center" justify="center" class="ma-10">
        Die Smartphone Version befindet sich noch in der Testphase.
        Bitte wechsel zu einem größeren Bildschirm oder maximiere das Fenster.
      </v-row>
      <v-row align="center" justify="center" class="ma-10">
        <v-icon large color="error">mdi-cellphone-off</v-icon>
      </v-row>
    </v-container>
    <MessageButton @onClickNewMessage="onMessageDialog"/>
    <SendMessageDialog ref="sendMessageDialog"/>
    <gobal-snackbar ref="globalSnackbar" />
    <footer-main class="mt-auto" />
  </v-app>
</template>

<script>
import TopMenuMain from '@/components/TopMenu.vue';
import MessageButton from '@/components/button/MessageButton.vue';
import SendMessageDialog from '@/components/dialog/SendMessageDialog.vue';
import FooterMain from '@/components/Footer.vue';
import GobalSnackbar from '@/components/modals/GlobalSnackbar.vue';

export default {
  name: 'Main',
  components: {
    TopMenuMain,
    FooterMain,
    GobalSnackbar,
    MessageButton,
    SendMessageDialog,
  },
  computed: {
    isMobile() {
      return this.$vuetify.breakpoint.smAndDown;
    },
  },
  methods: {
    onMessageDialog() {
      this.$refs.sendMessageDialog.open();
    },
  },
  mounted() {
    this.$root.globalSnackbar = this.$refs.globalSnackbar;
  },
};
</script>
