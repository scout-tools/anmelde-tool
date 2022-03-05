<template>
  <v-text-field
    v-model="data"
    :label="label"
    :prepend-icon="icon"
    :readonly="readonly"
    @change="onChange"
    :error-messages="error-messages"
  >
  <template slot="append">
    <v-btn icon v-if="edit" @click="onEditClick">
      <v-icon>mdi-pencil</v-icon>
    </v-btn>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-icon color="info" dark v-bind="attrs" v-on="on">
          mdi-help-circle-outline
        </v-icon>
      </template>
      <span>
        {{ tooltipText }}
      </span>
    </v-tooltip>
  </template>
  </v-text-field>
</template>

<script>
export default {
  props: ['data', 'label', 'icon', 'tooltipText', 'readonly', 'edit', 'type', 'error-messages'],
  methods: {
    onEditClick() {
      this.$emit('onEditClick');
    },
    onChange(newData) {
      this.$emit('update-data', this.type, newData);
    },
  },
};
</script>

<style>
</style>
