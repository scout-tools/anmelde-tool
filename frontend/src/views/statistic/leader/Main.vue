<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab>
      <v-icon left> mdi-table </v-icon>
      Tabelle
    </v-tab>
    <v-tab>
      <v-icon left> mdi-currency-eur </v-icon>
      Kasse
    </v-tab>
    <v-tab>
      <v-icon left> mdi-crowd </v-icon>
      Alter
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
          <Cash />
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
  </v-tabs>
</template>

<script>
import List from './tabs/List.vue';
import Cash from './tabs/Cash.vue';
import AgeGroup from './tabs/AgeGroup.vue';

export default {
  components: {
    List,
    Cash,
    AgeGroup,
  },
};
</script>
