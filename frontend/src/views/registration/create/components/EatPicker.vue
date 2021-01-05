<template>
<v-container fluid style="width:70%">
  <v-form v-model="valid">
    <v-row>
      <v-col col=12 class="mt-6">
        <v-slider
          v-model="total"
          color="black"
          label="Gesamt"
          min=0
          :max="total"
          thumb-label="always"
          readonly
        >
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="vegetarian"
          color="blue"
          label="Vegetarisch"
          min=0
          :max="maxVegetarian"
          thumb-label="always"
          type="number"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="vegan"
          color="green"
          label="Vegan"
          min=0
          :max="maxVegan"
          thumb-label="always"
          type="number"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="meatEater"
          color="brown"
          label="Fleischesser"
          min=0
          :max="total"
          thumb-label="always"
          readonly
        >
        </v-slider>
      </v-col>
    </v-row>
  </v-form>
</v-container>
</template>

<script>
export default {
  data: () => ({
    total: 20,
    vegetarian: 0,
    vegan: 0,
    valid: false,
  }),
  computed: {
    meatEater() {
      return this.total - this.vegetarian - this.vegan;
    },
    maxVegan() {
      return this.total - this.vegetarian;
    },
    maxVegetarian() {
      return this.total - this.vegan;
    },
    nameLabel() {
      return `${this.total} Wölflinge`;
    },
  },
};
</script>

<style scoped>
</style>
