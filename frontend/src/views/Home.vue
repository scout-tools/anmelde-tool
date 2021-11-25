<template>
  <v-app>
    <top-menu-main/>
    <router-view/>
    <footer-main class="mt-auto"/>
  </v-app>
</template>

<script>
import TopMenuMain from '@/components/TopMenu.vue';
import FooterMain from '@/components/Footer.vue';

export default {
  name: 'Main',
  components: {
    TopMenuMain,
    FooterMain,
  },
};
</script>
