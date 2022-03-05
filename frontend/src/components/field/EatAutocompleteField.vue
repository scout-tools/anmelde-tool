<template>
  <v-autocomplete
    v-model="value"
    :items="eatHabitTypeMapping"
    label="Essgewohnheiten"
    item-text="name"
    item-value="name"
    prepend-icon="mdi-food"
    multiple
    clearable
    chips
    @change="onInputChange"
  >
    <template slot="append">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="info" dark v-bind="attrs" v-on="on">
            mdi-help-circle-outline
          </v-icon>
        </template>
        <span>
          {{ toolTip }}
        </span>
      </v-tooltip>
    </template>
  </v-autocomplete>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  prop: ['value'],

  data: () => ({
    entries: [],
    isLoading: false,
    value: [],
    search: null,
    toolTip: 'Bitte wähle aus den angezeigten Essgewohnheiten.'
      + 'Weitere Essgewohnheiten können einfach durch Eingabe im Feld angegeben werden.',
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
