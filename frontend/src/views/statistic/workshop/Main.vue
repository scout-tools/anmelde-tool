<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab class="pa-2">
      <v-icon left> mdi-table-headers-eye </v-icon>
      Übersicht
    </v-tab>
    <!-- <v-tab>
      <v-icon left> mdi-table </v-icon>
      Details
    </v-tab> -->

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <!-- <OverviewMain /> -->
        </v-card-text>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <!-- <DetailMain /> -->
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
// import DetailMain from './tabs/details/Main.vue';
// import OverviewMain from './tabs/overview/Main.vue';

export default {
  components: {
    // OverviewMain,
    // DetailMain,
  },
};
</script>
