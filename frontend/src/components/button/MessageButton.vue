<template>
  <v-btn
    fab
    dark
    large
    color="success"
    fixed
    right
    bottom
    @click="onClickNewMessage"
  >
    <v-icon dark>message</v-icon>
  </v-btn>
</template>

<script>
export default {
  methods: {
    onClickNewMessage() {
      this.$emit('onClickNewMessage');
    },
  },
};
</script>

<style>
</style>
