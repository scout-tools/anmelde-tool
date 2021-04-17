<template>
      <v-tabs vertical>
        <v-tab>
          <v-icon left> mdi-table </v-icon>
          Tabelle
        </v-tab>
        <!-- <v-tab>
          <v-icon left> mdi-table-headers-eye </v-icon>
          Pivot
        </v-tab> -->

        <v-tab-item>
          <v-card flat>
            <v-card-text>
              <registration-overview/>
            </v-card-text>
          </v-card>
        </v-tab-item>

        <!-- <v-tab-item>
          <v-card flat>
            <v-card-text>
              <registration-table/>
            </v-card-text>
          </v-card>
        </v-tab-item> -->
      </v-tabs>
</template>

<script>
import RegistrationOverview from './RegistrationOverview.vue';
// import RegistrationTable from './RegistrationTable.vue';

export default {
  components: {
    // RegistrationTable,
    RegistrationOverview,
  },
};
</script>
