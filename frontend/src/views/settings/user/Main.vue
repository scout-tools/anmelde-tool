<template>
  <v-container>
    <v-row justify="center">
      <v-flex
        ma-3
        lg9
      >
    <v-layout column>
      <v-card>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="items.scoutName"
                  label="Pfadfindername">
                </v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  disabled
                  v-model="email"
                  label="Email Address">
                </v-text-field>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  v-model="items.mobileNumber"
                  label="Handynummer">
                </v-text-field>
              </v-col>
            </v-row>
            <v-row>
              <pick-stamm-form
                ref="pickStamm"
                @sendIdToParent="tranferId"
              />
            </v-row>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
                <v-text-field
                  disabled
                  v-model="getStammName"
                  label="Stamm">
                </v-text-field>
              </v-col>
              <v-col>
                <v-btn color="success" outlined tile @click="onPickStammClick()">
                    <v-icon left>mdi-pencil</v-icon>
                    Stamm bearbeiten
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-container>
            <v-row>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
            <v-btn color="success" @click="onSaveClicked">
                <v-icon left dark>mdi-check</v-icon>
                Änderungen speichern
            </v-btn>
              </v-col>
              <v-col
                cols="12"
                sm="6"
                md="4"
              >
            <v-btn dark color="red">
                <v-icon left>mdi-delete</v-icon>
                Account Daten löschen
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

import PickStammForm from './form/PickStamm.vue';

export default {
  components: {
    PickStammForm,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      items: [],
    };
  },
  computed: {
    getItems() {
      return this.items;
    },
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'herarchy',
    ]),
    email() {
      return this.getJwtData.email;
    },
    getStammName() {
      const obj = this.herarchy.find((user) => user.id === this.items.scoutOrganisation);
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
      this.saveUserData();
      this.$router.push({ name: 'eventOverview' });
    },
    getData() {
      const path = `${this.API_URL}auth/data/userextended/${this.getJwtData.user_id}/`;
      axios.get(path)
        .then((res) => {
          this.items = res.data;
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    saveUserData() {
      axios.put(`${this.API_URL}auth/data/userextended/${this.getJwtData.user_id}/`, {
        user: this.getJwtData.user_id,
        scoutOrganisation: this.items.scoutOrganisation,
        mobileNumber: this.items.mobileNumber,
        scoutName: this.items.scoutName,
      })
        .then(() => {
          this.showSuccess = true;
        })
        .catch(() => {
          this.showError = true;
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
