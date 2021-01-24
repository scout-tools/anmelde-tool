<template>
  <v-menu
    ref="menu"
    v-model="menu"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    min-width="auto"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-text-field
        v-model="date"
        label="Wähle das Geburtsdatum"
        prepend-icon="mdi-clock-time-four-outline"
        readonly
        v-bind="attrs"
        v-on="on"
      >
        <template slot="append">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon color="success" dark v-bind="attrs" v-on="on">
                mdi-help-circle-outline
              </v-icon>
            </template>
            <span>
              {{ 'Gallo' }}
            </span>
          </v-tooltip>
        </template>
      </v-text-field>
    </template>
    <v-date-picker
      ref="picker"
      v-model="date"
      :max="new Date().toISOString().substr(0, 10)"
      min="1950-01-01"
      @change="save"
    >
    </v-date-picker>
  </v-menu>
</template>

<script>
export default {
  data: () => ({
    date: new Date('Jan 2, 2010').toISOString().substr(0, 10),
    menu: false,
    tooltip: 'Gallo',
  }),
  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = 'YEAR')); // eslint-disable-line
    },
  },
  methods: {
    save(date) {
      this.$emit('input', this.date);
      this.$refs.menu.save(date);
    },
  },
};
</script>
