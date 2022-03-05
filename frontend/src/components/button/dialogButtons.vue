<template>
      <v-container class="py-0 px-1">
        <v-row>
          <v-col>
            <v-btn
              color="primary"
              @click="onClickCancel()"
              width="100%"
            >
              Cancel
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              color="primary"
              @click="onClickOk()"
              width="100%"
            >
              OK
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
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
