<template>
  <Pivot
    :data="data"
    v-model="fields"
    :reducer="reducer"
  />
</template>

<script>
import { mapGetters } from 'vuex';
import { Pivot } from 'vue-pivot-table-plus';

export default {
  components: { Pivot },
  data: () => { // eslint-disable-line
    return {

      fields: {
        availableFields: [],
        rowFields: [
          {
            getter: (item) => item.ageGroupPersonal,
            label: 'Alter',
          },
          {
            getter: (item) => item.habitTypePersonal,
            label: 'Typ',
          },
        ],
        colFields: [
        ],
        fieldsOrder: {},
      },
      reducer: (sum, item) => sum + item.numberPersonal, // eslint-disable-line
    };
  },
  computed: {
    ...mapGetters(['currentEventKitchen']),
    data() {
      return this.currentEventKitchen.numGroupedByAgePersonal;
    },
  },
};
</script>
