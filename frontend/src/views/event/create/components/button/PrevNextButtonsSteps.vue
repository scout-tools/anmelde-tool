<template>
  <v-row justify="center">
    <v-btn
      v-if="position > 1"
      class="mr-5"
      @click="$emit('prevStep')"
    >
      Zurück
    </v-btn>
    <v-btn
      v-if="position < maxPos"
      color="primary"
      @click="$emit('nextStep')"
    >
      Weiter
    </v-btn>
    <v-btn
      v-else
      color="primary"
      @click="$emit('submitStep')"
    >
      Abschließen
    </v-btn>
  </v-row>
</template>

<script>
export default {
  props: ['position', 'maxPos'],
};
</script>

<style scoped>

</style>
