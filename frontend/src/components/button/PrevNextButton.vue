<template>
  <v-row justify="center" class="ma-3">
    <v-btn v-if="position > 1 && maxPos > 1" class="mr-5" @click="goBack">
      <v-icon left> mdi-chevron-left</v-icon>
      Zurück
    </v-btn>
    <v-btn
      v-if="position < maxPos"
      color="primary"
      @click="goFurther"
    >
      Weiter
      <v-icon right> mdi-chevron-right</v-icon>
    </v-btn>
    <v-btn
      class="ml-2"
      icon
      v-if="position < maxPos && isDev"
      color="secondary"
      @click="$emit('ignore')"
    >
    <v-icon> mdi-debug-step-over</v-icon>
    </v-btn>
    <v-btn v-if="position >= maxPos" color="success" @click="submit">
      Abschließen
      <v-icon right>mdi-content-save</v-icon>
    </v-btn>
  </v-row>
</template>

<script>
export default {
  props: ['position', 'maxPos', 'valid'],
  computed: {
    isDev() {
      return process.env.VUE_APP_ENV === 'DEV';
    },
  },
  methods: {
    goFurther() {
      this.$emit('update');
      this.$emit('nextStep');
    },
    goBack() {
      this.$emit('update');
      this.$emit('prevStep');
    },
    submit() {
      this.$emit('update');
      this.$emit('submit');
    },
  },
};
</script>
