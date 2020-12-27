<template>
  <div class="about">
    <h1>Das ist die Seite mit der Anmeldungen</h1>
    <RegistrationCalender></RegistrationCalender>
    <RegistrationLineChart></RegistrationLineChart>
    <RegistrationStackedChart></RegistrationStackedChart>
  </div>
</template>

<script>
import RegistrationCalender from '@/views/statistic/registration/RegistrationCalender.vue';
import RegistrationLineChart from '@/views/statistic/registration/RegistrationLineChart.vue';
import RegistrationStackedChart from '@/views/statistic/registration/RegistrationStackedChart.vue';

export default {
  components: {
    RegistrationCalender,
    RegistrationLineChart,
    RegistrationStackedChart,
  },
};
</script>
