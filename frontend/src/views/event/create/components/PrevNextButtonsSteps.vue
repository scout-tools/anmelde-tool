<template>
  <v-row class="ma-3" justify="center">
    <v-btn
      v-if="position > 1"
      class="mr-5"
      @click="$emit('prevStep')"
    >
      Zurück
    </v-btn>
    <v-btn
      color="primary"
      @click="$emit('nextStep')"
    >
      Weiter
    </v-btn>
  </v-row>
</template>

<script>
export default {
  props: ['position'],
};
</script>

<style scoped>

</style>
