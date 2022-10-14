<template>
  <v-container class="mt-10">
    <v-row justify="center" class="mt-5">
      <v-flex ma-3>
        <v-layout column>
          <v-card>
            <v-tabs
              v-model="activeTab"
              background-color="primary"
              grow
              centered
              dark
              icons-and-text
            >
              <v-tabs-slider></v-tabs-slider>
              <v-tab v-for="tab in tabs" :key="tab.id" :to="tab.route" exact>
                {{ tab.name }}
                <v-icon>{{ tab.icon }}</v-icon>
              </v-tab>
            </v-tabs>
            <router-view></router-view>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters([]),
  },
  data() {
    return {
      activeTab: '/settings/user',
      tabs: [
        {
          id: 1,
          name: 'User',
          icon: 'mdi-clipboard-list',
          route: '/settings/user',
        },
        {
          id: 2,
          name: 'Person',
          icon: 'mdi-counter',
          route: '/settings/person',
        },
        {
          id: 3,
          name: 'Config',
          icon: 'mdi-card',
          route: '/settings/config',
        },
        {
          id: 4,
          name: 'DPV SSO',
          icon: 'mdi-key',
          route: '/settings/sso',
        },
      ],
      eventOverview: [],
    };
  },
  methods: {},
};
</script>
