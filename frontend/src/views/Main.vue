<template>
  <v-app>
    <top-menu-main v-show="!isLoginOnly"/>
    <div v-if="isRouterPageUndefined" class="fullsize pa-10">
      <v-btn
        class="ma-10"
        @click="onRefreshClicked"
        color="primary"
      >
        Weiter
      </v-btn>
    </div>
    <router-view class="fullsize"/>
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
    isRouterPageUndefined() {
      return this.$router.history.current.name === null;
    },
    isLoginOnly() {
      return this.$router.history.current.query.header === 'no';
    },
  },
  methods: {
    onRefreshClicked() {
      this.$router.go();
    },
    onGoToStartpageClicked() {
      this.$router.go();
    },
  },
};
</script>

<style scoped>
.fullsize{
  min-height: 95vh !important;
}</style>
