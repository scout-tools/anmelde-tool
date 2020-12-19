<template>
  <v-card
    max-width="600"
    class="mx-auto"
  >
    <v-card-title class="text-center justify-center py-6">
      Deine Veranstaltungen
    </v-card-title>

      <v-container fluid>
        <v-row>
          <v-col cols="5" class="ma-3">
            <v-switch
              label="Alte Aktionen"
              color="blue"
            ></v-switch>
          </v-col>
          <v-col cols="5" class="ma-3">
            <v-switch
              label="Zukunfte Aktionen"
              color="green"
              hide-details
            ></v-switch>
          </v-col>
        </v-row>
      </v-container>
    <v-list
      subheader
      two-line
    >
      <v-subheader inset>Hier kannst du alle deine Buchbaren Veranstaltungen sehen</v-subheader>
      <template
        v-for="(item, index) in getItems"
      >
      <v-list-item
        :key="item.name"
      >
        <v-list-item-avatar>
          <v-icon color="green">mdi-tent</v-icon>
        </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title v-text="item.name"></v-list-item-title>

                <v-list-item-subtitle
                  class="text--primary"
                >{{ getText(item) }}</v-list-item-subtitle>

                <v-list-item-subtitle v-text="item.description"></v-list-item-subtitle>
              </v-list-item-content>

        <v-list-item-action>
          <v-btn icon @click="onRegistrationClicked">
            <v-icon color="primary">mdi-account-multiple-plus</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
          <v-divider
            v-if="index < getItems.length - 1"
            :key="index"
          ></v-divider>
  </template>
    </v-list>
  </v-card>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    headers: [
      { text: 'Id', value: 'id' },
      { text: 'Fahrt/Lager', value: 'name' },
      { text: 'Beschreibung', value: 'description' },
      { text: 'Actions', value: 'action', sortable: false },
    ],
  }),

  computed: {
    getItems() {
      // this.messages.forEach((value) => console.log(value));
      return this.items;
    },
  },
  methods: {
    getText(item) {
      const startTime = new Date(item.startTime);
      const endTime = new Date(item.endTime);
      const dateFormat = 'll';

      return `${moment(startTime).format(dateFormat)} bis ${moment(endTime).format(dateFormat)}`;
    },
    getData() {
      const path = `${this.API_URL}basic/event/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    show(item) {
      this.$refs.messageModal.show(item);
    },
    onRegistrationClicked() {
      this.$router.push({ name: 'registrationForm' });
    },
  },
  created() {
    this.getData();
  },
};
</script>
