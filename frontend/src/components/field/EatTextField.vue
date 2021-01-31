<template>
  <v-text-field
    v-model="value"
    label="Essens Besonderheiten (Freitext)"
    prepend-icon="mdi-food"
    clearable
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
  </v-text-field>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  prop: ['value'],

  data: () => ({
    isLoading: false,
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
