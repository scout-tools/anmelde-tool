<template>
  <div class="text-center ma-5">
    <p>{{ text }}</p>
    <v-progress-circular
      :size="80"
      :width="10"
      class="ma-5"
      :color="save ? 'success' : 'primary'"
      indeterminate
    ></v-progress-circular>
    <p>Bitte hab etwas Geduld.</p>
  </div>
</template>

<script>
export default {
  props: {
    save: {
      default: false,
    },
  },
  computed: {
    text() {
      return this.save ? 'Speichere Daten ...' : 'Lade Daten ...';
    },
  },
};
</script>

<style>
</style>
