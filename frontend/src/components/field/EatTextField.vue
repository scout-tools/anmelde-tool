<template>
  <v-combobox
    v-model="value"
    label="Essgewohnheiten (Freitext)"
    prepend-icon="mdi-food"
    :items="items"
    clearable
    multiple
    chips
    @change="onInputChange"
  >
    <template slot="append">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="success" dark v-bind="attrs" v-on="on">
            mdi-help-circle-outline
          </v-icon>
        </template>
        <span>
          {{ toolTipTextField }}
        </span>
      </v-tooltip>
    </template>
  </v-combobox>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  prop: ['value'],

  data: () => ({
    isLoading: false,
    items: [],
    value: '',
    toolTipTextField: 'Bitte trage hier ein, auf welche Besonderheiten die Küche achten muss.'
      + 'Trage hier nur etwas ein, wenn die Optionen des anderen Feldes nicht zutreffen',
  }),
  computed: {
    ...mapGetters(['eatHabitTypeMapping']),
  },
  methods: {
    onInputChange() {
      this.$emit('input', this.value);
    },
    setValue(value) {
      this.value = value;
    },
  },
};
</script>
