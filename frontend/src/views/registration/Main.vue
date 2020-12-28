<template>
  <v-container>
    <v-row justify="center">
      <v-flex ma-3 lg9>
        <v-layout column>
          <v-card>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field disabled v-model="items.scoutName" label="Mein Name">
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field disabled v-model="getStammName" label="Mein Stamm">
                    </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field
                      v-model="items.invitationCode"
                      label="Einladungscode vom Veranstalter"
                    >
                    </v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-btn color="success" @click="onSaveClicked">
                      <v-icon left dark>mdi-check</v-icon>
                      Ich möchte den Anmeldeprozess jetzt starten
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-layout>
      </v-flex>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      items: [],
      reg_id: null,
    };
  },
  computed: {
    getItems() {
      return this.items;
    },
    ...mapGetters(['isAuthenticated', 'getJwtData', 'hierarchy']),
    email() {
      return this.getJwtData.email;
    },
    getStammName() {
      const obj = this.hierarchy.find((user) => user.id === this.items.scoutOrganisation);
      if (obj && obj.name) {
        return obj.name;
      }
      return 'Kein Stamm';
    },
  },
  methods: {
    tranferId(id) {
      this.items.scoutOrganisation = id;
    },
    onPickStammClick() {
      this.$refs.pickStamm.show(this.items.scoutOrganisation);
    },
    onSaveClicked() {
      this.createRegestration();
    },
    getData() {
      this.loadUserExtended();
    },
    loadUserExtended() {
      const path = `${this.API_URL}auth/data/user-extended/${this.getJwtData.userId}/`;
      axios
        .get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    createRegestration() {
      const eventId = this.$route.params.id;
      axios
        .post(`${this.API_URL}basic/registration/`, {
          responsiblePersons: this.getJwtData.userId,
          scoutOrganisation: this.items.scoutOrganisation,
          event: eventId,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationCreate',
            params: {
              id: response.data.id,
              event: response.data.event,
            },
          });
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
