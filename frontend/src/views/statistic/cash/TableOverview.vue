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
            getter: (item) => item.scoutOrganisation_Name,
            label: 'Stamm',
          },
          {
            getter: (item) => `${item.totalAmount} Pers`,
            label: 'Anzal',
          },
        ],
        colFields: [
        ],
        fieldsOrder: {},
      },
      reducer: (sum, item) => sum + item.totalFee, // eslint-disable-line
      tableHeight: '400px',
    };
  },
  computed: {
    ...mapGetters(['currentEventCash']),
    data() {
      return this.currentEventCash[0].groupedParticipants;
    },
  },
};
</script>
