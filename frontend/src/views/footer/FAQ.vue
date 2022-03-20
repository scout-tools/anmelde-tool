<template>
  <v-container class="top-margin">
    <v-row class="center text-center justify-center">
      <p>
        Bei Fragen aller Art könnt ihr euch bei uns melden:
        <br/>
        <img
          alt="Email Adresse für Support Anfragen "
          class="mr-2"
          :src="require('@/assets/anmeldeToolMailAdresse.jpg')"
          height="50"
        /></p
      ></v-row>
    <v-row class="center text-center justify-center">
      <v-divider/>
      <v-expansion-panels>
        <v-expansion-panel v-for="(faq, i) in faqs" :key="i">
          <v-expansion-panel-header>
            <span class="title ma-3"> {{ faq.question }}</span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <p class="text-left subtitle-1 pa-3" v-html="faq.answer"></p>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    faqs: [],
  }),
  created() {
    const path = `${process.env.VUE_APP_API}/basic/faq/`;
    axios.get(path)
      .then((success) => {
        this.faqs = success.data;
      });
  },
};
</script>
