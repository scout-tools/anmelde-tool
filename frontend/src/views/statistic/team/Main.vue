<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab>
      <v-icon left> mdi-table </v-icon>
      Tabelle
    </v-tab>
    <v-tab>
      <v-icon left> mdi-crowd </v-icon>
      Alter
    </v-tab>
    <v-tab>
      <v-icon left> mdi-food </v-icon>
      Essen
    </v-tab>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <List />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <AgeGroup />
        </v-card-text>
      </v-card>
    </v-tab-item>
     <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Food />
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import List from './tabs/List.vue';
import AgeGroup from './tabs/AgeGroup.vue';
import Food from './tabs/Food.vue';

export default {
  components: {
    List,
    AgeGroup,
    Food,
  },
};
</script>
