<template>
  <v-card class="mx-auto" :color="color" dark max-width="400">
    <v-list-item two-line>
      <v-list-item-content>
        <v-list-item-title class="headline">{{
          data.header
        }}</v-list-item-title>
        <v-list-item-subtitle>{{ data.subheader }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item dense v-for="(item, index) in list" :key="index">
      <v-list-item-icon>
        <v-icon>mdi-account-group</v-icon>
      </v-list-item-icon>
      <v-list-item-subtitle
        v-if="data.rankField === 'updatedAt'"
        v-text="formatData(item[data.rankField])"
      />
      <v-list-item-subtitle
        v-if="data.rankField !== 'updatedAt'"
        v-text="item[data.rankField]"
      />
      <v-list-item-subtitle>{{ item.scoutOrganisation }} </v-list-item-subtitle>
    </v-list-item>

    <!-- <v-divider></v-divider>

    <v-card-actions>
      <v-btn text> Full Report </v-btn>
    </v-card-actions> -->
  </v-card>
</template>

<script>
import moment from 'moment';

export default {
  props: ['data', 'color'],
  computed: {
    list() {
      const xx = this._.orderBy(
        this.data.dataOne,
        [this.data.rankField],
        [this.data.rankOrder],
      ).slice(0, 5);
      debugger;
      return xx;
    },
  },
  methods: {
    formatData(item) {
      return moment(item).format(this.dateFormat);
    },
  },
  data() {
    return {
      dateFormat: 'DD.MM.YYYY',
    };
  },
};
</script>
