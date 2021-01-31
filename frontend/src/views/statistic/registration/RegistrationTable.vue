<template>
  <Pivot
    :data="data"
    v-model="fields"
    :reducer="reducer"
    :showSettings="defaultShowSettings"
  />
</template>

<script>
import { mapGetters } from 'vuex';
import { Pivot } from 'vue-pivot-table-plus';

export default {
  name: 'RegistrationCalender',
  components: { Pivot },
  data: () => { // eslint-disable-line
    return {
      defaultShowSettings: true,
      fields: {
        availableFields: [],
        rowFields: [
          {
            getter: (item) => item.scoutOrganisation_Name,
            label: 'Stamm',
          },
          {
            getter: (item) => item.bund,
            label: 'Bund',
            showHeader: false,
          },
        ],
        colFields: [
        ],
        fieldsOrder: {},
      },
      reducer: (sum, item) => sum + item.participants, // eslint-disable-line
      tableHeight: '400px',
    };
  },
  computed: {
    ...mapGetters(['currentEventParticipants']),
    data() {
      return this.currentEventParticipants[0].scoutOrganisations;
    },
  },
};
</script>
