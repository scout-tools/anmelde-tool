<template>
  <div>
    <div>
      <v-btn
        color="primary"
        @click="onClickCancel()"
        width="100%"
      >
        Cancel
      </v-btn>
    </div>
    <div>
      <v-btn
        color="primary"
        @click="onClickOk()"
        width="100%"
      >
        OK
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    onClickOk() {
      this.$emit('ok');
    },
    onClickCancel() {
      this.$emit('cancel');
    },
  },
};
</script>
