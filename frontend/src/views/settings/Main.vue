<template>
  <v-container class="mt-10">
    <v-row justify="center" class="mt-5">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card>
            <v-tabs
              v-model="tab"
              background-color="primary"
              grow
              centered
              dark
              icons-and-text
            >
              <v-tabs-slider></v-tabs-slider>

              <v-tab
                href="#tab-1"
              >
                Persönlich
                <v-icon>mdi-clipboard-list</v-icon>
              </v-tab>

              <v-tab
                href="#tab-2"
              >
                Einstellungen
                <v-icon>mdi-counter</v-icon>
              </v-tab>
            </v-tabs>

            <v-tabs-items v-model="tab">
              <v-tab-item v-for="i in 6" :key="i" :value="'tab-' + i">
                <v-card-text>
                  <UserMain v-if="i === 1" />
                  <ConfigMain v-if="i === 2" />
                </v-card-text>
              </v-tab-item>
            </v-tabs-items>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

import ConfigMain from './config/Main.vue';
import UserMain from './user/Main.vue';

export default {
  components: {
    ConfigMain,
    UserMain,

  },
  computed: {
    ...mapGetters([
    ]),
    eventId() {
      return this.$route.params.id;
    },
  },
  data() {
    return {
      tab: 1,
      eventOverview: [],
    };
  },
  methods: {
  },
};
</script>
