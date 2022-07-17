<template>
  <v-container>
    <div v-if="!loading">
      <v-tabs vertical text class="pa-0">
        <v-tab v-for="(item,index) in data" :key="index">
          {{ item.title }}
        </v-tab>
        <v-tab-item v-for="(item,index) in data" :key="index">
          <v-card flat>
            <v-card-text>
              <IntegerAttribute :attribute="item"
                                v-if="item.attribute.resourcetype === 'IntegerAttribute'"/>
              <TravelAttribute :attribute="item"
                               v-else-if="item.attribute.resourcetype === 'TravelAttribute'"/>
              <TravelAttributeV2 :attribute="item"
                               v-else-if="item.attribute.resourcetype === 'TravelAttributeV2'"/>
              <BooleanAttribute :attribute="item"
                                v-else-if="item.attribute.resourcetype === 'BooleanAttribute'"/>
              <StringAttribute :attribute="item"
                               v-else-if="item.attribute.resourcetype === 'StringAttribute'"/>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs>
    </div>
    <div v-else>
      <div class="text-center ma-5">
        <p>Lade Daten ...</p>
        <v-progress-circular
          :size="80"
          :width="10"
          class="ma-5"
          color="primary"
          indeterminate
        ></v-progress-circular>
        <p>Bitte hab etwas Geduld.</p>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios';
import BooleanAttribute from './tabs/BooleanAttribute.vue';
import StringAttribute from './tabs/StringAttribute.vue';
import TravelAttribute from './tabs/TravelAttribute.vue';
import TravelAttributeV2 from './tabs/TravelAttributeV2.vue';
import IntegerAttribute from './tabs/IntegerAttribute.vue';

export default {
  components: {
    StringAttribute,
    BooleanAttribute,
    TravelAttribute,
    TravelAttributeV2,
    IntegerAttribute,
  },
  data: () => ({
    data: [],
    loading: true,
    errormsg: '',
  }),
  methods: {
    getData(eventId) {
      this.loading = true;
      this.getAttributeSummary(eventId)
        .then((responseObj) => {
          this.data = responseObj.data;
        })
        .catch((error) => {
          console.log(error);
          this.errormsg = error.response.data.message;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    async getAttributeSummary(eventId) {
      const path = `${process.env.VUE_APP_API}/event/event/${eventId}/summary/attributes/`;
      return axios.get(path);
    },
  },
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
