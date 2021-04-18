<template>
  <v-card class="mx-auto" :color="color" dark max-width="400">
    <v-list-item two-line>
      <v-list-item-content>
        <v-list-item-title class="headline">{{ data.header }}</v-list-item-title>
        <v-list-item-subtitle>{{ data.subheader }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-card-text>
      <v-row align="center">
        <v-col class="display-3" cols="6">{{ data.dataOne }}</v-col>
        <v-col class="display-3" cols="6">{{ data.dataTwo }}</v-col>
      </v-row>
      <v-row align="center">
        <v-col cols="6">{{ data.dataOneName }}</v-col>
        <v-col cols="6">{{ data.dataTwoName }}</v-col>
      </v-row>
    </v-card-text>

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
