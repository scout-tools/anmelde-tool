<template>
  <v-app>
    <top-menu-main/>
    <router-view />
    <footer-main/>
  </v-app>
</template>

<script>
import axios from 'axios';
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
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
  }),
  methods: {
    getHierarchy() {
      const path = `${process.env.VUE_APP_API}basic/scout-hierarchy/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setHierarchy', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
    getAgeGroup() {
      const path = `${this.API_URL}basic/age-group/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setAgeGroupMapping', res.data);
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getHierarchy();
    this.getAgeGroup();
  },
};
</script>

<style scoped></style>
