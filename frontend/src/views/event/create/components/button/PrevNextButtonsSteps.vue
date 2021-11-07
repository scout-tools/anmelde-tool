<template>
  <v-container>
    <v-row justify="center" class="ma-3">
      <v-btn v-if="position > 1" class="mr-5" @click="$emit('prevStep')">
        <v-icon left> mdi-chevron-left </v-icon>
        Zurück
      </v-btn>
      <v-btn
        v-if="position < maxPos"
        color="primary"
        @click="$emit('nextStep')"
      >
        Weiter
        <v-icon right> mdi-chevron-right </v-icon>
      </v-btn>
      <v-btn v-else color="primary" @click="$emit('submitStep')">
        Abschließen
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: ['position', 'maxPos'],
};
</script>
