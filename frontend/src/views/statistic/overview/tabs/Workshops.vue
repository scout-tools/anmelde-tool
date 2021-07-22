<template>
<v-container fluid class="pa-0">
<v-row justify="center" class="overflow-y: auto">
  <v-data-table
    :headers="headers"
    :items="getItems()"
    show-expand
    class="w-75"
  >
    <template v-slot:item.costs="{ item }">
      {{ item.costs }} €
    </template>
    <template v-slot:expanded-item="{ headers, item }">
      <td :colspan="headers.length">
        <p class="pt-3">
        {{ item.freeText }}
        </p>
      </td>
    </template>
  </v-data-table>
</v-row>
</v-container>
</template>

<script>
import { serviceMixin } from '@/mixins/serviceMixin';

export default {
  mixins: [serviceMixin],
  data: () => ({
    data: [],
    headers: [
      { text: 'AG-Name', value: 'title' },
      { text: 'Kosten', value: 'costs' },
      { text: 'Verantwortlicher', value: 'supervisorName' },
    ],
  }),
  methods: {
    getItems() {
      return this.data;
    },
    async getData() {
      const { data } = await this.getWorkshopStats();
      this.data = data;
    },
  },
  created() {
    this.getData();
  },
};
</script>

<style scoped>
.w-75 {
  width: 75%;
}
</style>
