<template>
  <v-app>
    <top-menu-main v-show="!isLoginOnly"/>
    <router-view />
    <footer-main v-show="!isLoginOnly"/>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';

import TopMenuMain from '@/components/TopMenu.vue';
import FooterMain from '@/components/Footer.vue';

export default {
  name: 'Main',
  components: {
    TopMenuMain,
    FooterMain,
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'getJwtData']),
    userName() {
      return this.getJwtData.email;
    },
    isSimpleUser() {
      if (this.getJwtData) {
        return !(this.getJwtData.groups.length || this.getJwtData.isStaff);
      }
      return true;
    },
    isLoginOnly() {
      return this.$router.history.current.query.header === 'no';
    },
  },
};
</script>

<style scoped></style>
