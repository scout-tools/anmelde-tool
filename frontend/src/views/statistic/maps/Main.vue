<template>
  <v-tabs vertical icons-and-text>
    <v-tab>
      <v-icon left>mdi-map-search</v-icon>
      Details
    </v-tab>
    <v-tab>
      <v-icon left> mdi-map </v-icon>
      Übersicht
    </v-tab>

    <v-tab-item>
      <v-card flat class="ma-0">
        <v-card-text class="ma-0">
          <OsmMap />
        </v-card-text>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat class="ma-0">
        <v-card-text class="ma-0">
          <SimpleMap />
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import OsmMap from './OsmMap.vue';
import SimpleMap from './MapGermany.vue';

export default {
  components: {
    OsmMap,
    SimpleMap,
  },
};
</script>
