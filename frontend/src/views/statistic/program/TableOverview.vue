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
  name: 'RegistrationProgram',
  components: { Pivot },
  data: () => { // eslint-disable-line
    return {

      fields: {
        availableFields: [],
        rowFields: [
          {
            getter: (item) => item.ageGroup,
            label: 'Alter',
          },
          {
            getter: (item) => item.role,
            label: 'Fahrt',
          },
        ],
        colFields: [
        ],
        fieldsOrder: {},
      },
      reducer: (sum, item) => sum + item.numberGroup + item.numberPersonal, // eslint-disable-line
    };
  },
  computed: {
    ...mapGetters(['currentEventProgram']),
    data() {
      return this.currentEventProgram[0].participantsGroupedByAge;
    },
  },
};
</script>
