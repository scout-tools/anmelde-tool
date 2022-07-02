<template>
  <v-list>
    <v-subheader
      >Bitte verteile alle angemeldeten
      {{ summaryData.participantCount }} Personen.
    </v-subheader
    >
    <v-list-item-group color="primary" :value="item" @change="onInputChanged">
      <v-list-item v-for="(item, i) in items" :key="i">
        <v-list-item-avatar>
          <v-icon color="black" dark>{{ getTypeIcon(item.typeField) }}</v-icon>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>
            {{ getText(item) }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="!items.length">
        Kein Eintrag vorhanden.
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  data: () => ({
  }),
  props: {
    items: {
      default: [],
    },
    summaryData: {
      default: {},
    },
    item: {
      default: null,
    },
  },
  watch: {
  },
  methods: {
    onInputChanged(value) {
      this.$emit('onItemChanged', value);
    },
    getTypeIcon(key) {
      const mapping = {
        Bahn: 'mdi-train',
        Reisebus: 'mdi-bus',
        PKW: 'mdi-car',
        Sonstiges: 'mdi-help-rhombus',
      };
      return mapping[key];
    },
    getText(item) {
      return `${item.numberPersons} Personen mit ${
        item.typeField
      } am ${this.$moment(item.dateTimeField).format('DD.MM.YY HH:mm')}`;
    },
  },
};
</script>

<style>
</style>
