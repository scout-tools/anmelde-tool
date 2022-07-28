<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab>
      <v-icon left> mdi-table</v-icon>
      Tabelle
    </v-tab>
    <v-tab>
      <v-icon left> mdi-food</v-icon>
      Essen
    </v-tab>
    <v-tab>
      <v-icon left> mdi-crowd</v-icon>
      Alter
    </v-tab>
    <v-tab>
      <v-icon left> mdi-beer</v-icon>
      Alkohol
    </v-tab>
    <v-tab>
      <v-icon left> mdi-chevron-triple-up</v-icon>
      Amt
    </v-tab>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <List/>
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Food/>
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <AgeGroup/>
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <AlcoholAgeGroup/>
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <LeaderTypes/>
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import LeaderTypes from '@/views/statistic/team/tabs/LeaderTypes.vue';

import AlcoholAgeGroup from '@/views/statistic/team/tabs/AlcoholAgeGroup.vue';
import List from './tabs/List.vue';
import AgeGroup from './tabs/AgeGroup.vue';
import Food from './tabs/Food.vue';

export default {
  components: {
    List,
    AgeGroup,
    Food,
    LeaderTypes,
    AlcoholAgeGroup,
  },
};
</script>
