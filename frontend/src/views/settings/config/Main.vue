<template>
  <v-card flat>
    <v-card-title class="text-center justify-center py-6">
      Hier kannst du deine Einstellungen anpassen.
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-subheader class="ma-5"> Wähle dein Farbschema aus. </v-subheader>
        <v-row>
          <v-col cols="12" sm="6">
            <v-select
              label="Farbschemen"
              :items="themeOptions"
              v-model="theme"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      themeOptions: [
        {
          text: 'Normal',
          value: 'default',
        },
        {
          text: 'DPV-Gold',
          value: 'dpvgold',
        },
        {
          text: 'DPBM',
          value: 'mosaik',
        },
      ],
    };
  },
  computed: {
    theme: {
      get() {
        return this.$store.state.preferences.theme;
      },
      set(theme) {
        this.$store.commit('setTheme', theme);
      },
    },
  },
};
</script>

<style>
</style>
