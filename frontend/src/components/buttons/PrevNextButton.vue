<template>
  <v-row justify="center" class="ma-3">
    <v-btn v-if="position > 1 && maxPos > 1" class="mr-5" @click="$emit('prevStep')">
      <v-icon left> mdi-chevron-left</v-icon>
      Zurück
    </v-btn>
    <v-btn v-if="position < maxPos" color="primary" @click="$emit('update')&&$emit('nextStep')">
      Weiter
      <v-icon right> mdi-chevron-right</v-icon>
    </v-btn>
    <v-btn class="ml-2"
           icon
           v-if="position < maxPos"
           color="primary"
           @click="$emit('ignore')">
      <v-icon right> mdi-debug-step-over</v-icon>
    </v-btn>
    <v-btn v-else color="success" @click="$emit('update')&&$emit('submitStep')">
      Abschließen
      <v-icon right>mdi-content-save</v-icon>
    </v-btn>
  </v-row>
</template>

<script>
export default {
  props: ['position', 'maxPos'],
};
</script>
