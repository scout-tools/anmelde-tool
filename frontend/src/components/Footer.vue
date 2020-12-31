<template>
  <div>
    <v-footer color="primary lighten-1" padless absolute>
      <v-row justify="center" no-gutters>
        <v-btn
        color="white"
        text
        rounded
        class="my-2"
        @click="$router.push({ name: 'impressum' })"
      >
          Impressum
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'contact' })"
        >
          Kontakt
        </v-btn>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'loginInterals' })"
        >
          Planungsjurte
        </v-btn>
        <v-col class="primary lighten py-4 text-center white--text" cols="12">
          {{ new Date().getFullYear() }} — <strong>Anmelde-Tool</strong>
        </v-col>
      </v-row>
    </v-footer>
  </div>
</template>

<script>
export default {
  data: () => ({
    links: ['Impressum', 'Kontakt', 'Planungsjurte'],
  }),
};
</script>

<style></style>
