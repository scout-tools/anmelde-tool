<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center pa-0">
      <v-card class="mx-auto pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
              </v-col>
              <v-col cols="12" md="6">
              </v-col>
            </v-row>
            <v-row class="pa-0">
              <v-col cols="12" md="6">
              </v-col>
              <v-col cols="12" md="6">
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
import { serviceMixin } from '@/mixins/serviceMixin';

export default {
  mixins: [serviceMixin],
  components: {
  },
  data: () => ({
    data: [],
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
  },
  methods: {
  },
  created() {
  },
};
</script>
