<template>
  <div>
    <v-card
      v-for="item in anz"
      v-bind:key="item"
      class="ml-3 mt-4 d-inline-block"
      width="370px"
      height="195px"
      color="purple"
      outlined
    >
      <v-card-text>
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
        sed diam nonumy eirmod tempor invidunt ut labore et dolore
        magna aliquyam erat, sed diam voluptua.
      </v-card-text>
    </v-card>
    <v-card
      v-bind:key="item"
      class="ml-3 mt-4 d-inline-block html2pdf__page-break"
      width="370px"
      height="195px"
      color="purple"
      outlined
    >
      <v-card-text>
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
        sed diam nonumy eirmod tempor invidunt ut labore et dolore
        magna aliquyam erat, sed diam voluptua.
      </v-card-text>
    </v-card>
    <v-card
      v-bind:key="item"
      class="ml-3 mt-4 d-inline-block"
      width="370px"
      height="195px"
      color="purple"
      outlined
    >
      <v-card-text>
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
        sed diam nonumy eirmod tempor invidunt ut labore et dolore
        magna aliquyam erat, sed diam voluptua.
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    anz: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
  }),
};
</script>
