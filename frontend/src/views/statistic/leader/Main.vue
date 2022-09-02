<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab>
      <v-icon left> mdi-table</v-icon>
      Tabelle
    </v-tab>
    <v-tab>
      <v-icon left> mdi-currency-eur</v-icon>
      Kasse
    </v-tab>
    <v-tab>
      <v-icon left>mdi-download</v-icon>
      Downloads
    </v-tab>
    <v-tab>
      <v-icon left>mdi-email</v-icon>
      Email Export
    </v-tab>
    <v-tab>
      <v-icon left> mdi-tools </v-icon>
      Bearbeiten
    </v-tab>
    <v-tab>
      <v-icon left> mdi-plus </v-icon>
      Hinzufügen
    </v-tab>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <List />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Cash />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Download />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <Email />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <EditReg />
        </v-card-text>
      </v-card>
    </v-tab-item>
    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <NewReg />
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import List from './tabs/List.vue';
import Cash from './tabs/Cash.vue';
import Download from './tabs/Download.vue';
import Email from './tabs/Email.vue';
import EditReg from './tabs/EditReg.vue';
import NewReg from './tabs/NewReg.vue';

export default {
  components: {
    List,
    Cash,
    Download,
    Email,
    EditReg,
    NewReg,
  },
};
</script>
