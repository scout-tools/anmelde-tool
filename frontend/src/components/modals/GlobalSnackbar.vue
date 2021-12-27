<template>
  <v-snackbar
    :color="color"
    :timeout="timer"
    v-model="showSnackbar"
    bottom>
    <v-icon left>{{ icon }}</v-icon>
    {{ message }}
  </v-snackbar>
</template>

<script>
export default {
  name: 'GobalSnackbar',
  data() {
    return {
      showSnackbar: false,
      message: '',
      color: 'success',
      icon: 'mdi-check',
      timer: 3000,
    };
  },
  methods: {
    show(data) {
      this.message = data.message || 'missing "message".';
      this.color = data.color || 'success';
      this.timer = data.timer || 3000;
      this.icon = data.icon || 'mdi-check';
      this.showSnackbar = true;
    },
  },
};
</script>
