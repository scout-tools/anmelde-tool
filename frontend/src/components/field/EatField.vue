<template>
  <v-combobox
    v-model="model"
    :items="items"
    label="Essens Besonderheiten"
    item-text="name"
    item-value="id"
    prepend-icon="mdi-food"
    return-object
    multiple
    clearable
    chips
  >
    <template slot="append">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="success" dark v-bind="attrs" v-on="on">
            mdi-help-circle-outline
          </v-icon>
        </template>
        <span>
          {{ tooltip }}
        </span>
      </v-tooltip>
    </template>
  </v-combobox>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    entries: [],
    isLoading: false,
    model: [],
    search: null,
    tooptip: 'Bitte trage hier ein, auf welche Besonderheiten die Küche achten muss.',
  }),
  computed: {
    ...mapGetters(['eatHabitTypeMapping']),

    items() {
      if (!this.model.filter((item) => item.id === 2).length) {
        return this.eatHabitTypeMapping;
      }
      return this.eatHabitTypeMapping
        .filter((item) => item.id !== 5)
        .filter((item) => item.id !== 6)
        .filter((item) => item.id !== 1);
    },
  },
};
</script>
