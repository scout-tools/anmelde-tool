<template>
  <v-card class="mx-auto" :color="color" dark max-width="400">
    <v-list-item two-line>
      <v-list-item-content>
        <v-list-item-title class="headline">{{ data.header }}</v-list-item-title>
        <v-list-item-subtitle>{{ data.subheader }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item dense v-for="(item, index) in data.dataOne" :key="index">
      <v-list-item-icon>
        <v-icon>mdi-account-group</v-icon>
      </v-list-item-icon>
      <v-list-item-subtitle>{{ item.scoutOrganisation}} </v-list-item-subtitle>
    </v-list-item>

    <!-- <v-divider></v-divider>

    <v-card-actions>
      <v-btn text> Full Report </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script>
export default {
  props: ['data', 'color'],
  data: () => ({
  }),
};
</script>
