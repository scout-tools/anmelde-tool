<template>
  <div>
    <v-footer color="primary lighten-1">
      <v-row justify="center" no-gutters>
        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'impressum' })">
          <v-icon fab color="white" class="mr-1">
            mdi-card-text-outline
          </v-icon>
          Impressum
        </v-btn>

        <v-btn
          color="white"
          text
          rounded
          class="my-2"
          @click="$router.push({ name: 'datenschutz' })">
          <v-icon fab color="white" class="mr-1">
            mdi-fingerprint
          </v-icon>
          Datenschutz
        </v-btn>
      </v-row>
    </v-footer>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data: () => ({
    links: ['Impressum', 'Kontakt', 'Planungsjurte'],
  }),
};
</script>
