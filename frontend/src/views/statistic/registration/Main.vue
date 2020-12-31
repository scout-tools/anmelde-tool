<template>
  <div>
    <registration-calender/>
    <registration-line-chart/>
    <registration-stacked-chart/>
  </div>
</template>

<script>
import RegistrationCalender from './RegistrationCalender.vue';
import RegistrationLineChart from './RegistrationLineChart.vue';
import RegistrationStackedChart from './RegistrationStackedChart.vue';

export default {
  components: {
    RegistrationLineChart,
    RegistrationStackedChart,
    RegistrationCalender,
  },
};
</script>
