<template>
  <v-container>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        transition="dialog-top-transition"
        fullscreen
        hide-overlay
      >
        <v-card>
       <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="cancel"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Wähle deinen Stamm aus</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-toolbar-items>
           <v-btn
              :disabled="!selected"
              class="white--text"
              color="green darken-1"
              depressed
              @click="onTakeStammClicked"
            >
              Das ist mein Stamm
              <v-icon right> mdi-content-save </v-icon>
            </v-btn>
          </v-toolbar-items>
        </v-toolbar>
          <v-row class="pa-4" justify="space-between">
            <v-col cols="5">
              <v-text-field
                v-model="search"
                label="Suche einen Stamm"
                flat
                clearable
                clear-icon="mdi-close-circle-outline"
              ></v-text-field>
              <v-treeview
                :active.sync="active"
                :items="hierarchyNested"
                :open.sync="open"
                activatable
                :search="search"
                color="warning"
                open-on-click
                transition
              >
              </v-treeview>
            </v-col>

            <v-divider vertical></v-divider>

            <v-col class="d-flex text-center">
              <v-scroll-y-transition mode="out-in">
                <div
                  v-if="!selected"
                  class="title grey--text text--lighten-1 font-weight-light"
                >
                  Wähle einen Stamm
                </div>
                <v-card
                  v-else
                  :key="selected.id"
                  min-width="300"
                  class="mx-auto"
                  flat
                >
                  <v-card-text>
                    <h3 class="headline mb-2">
                      {{ selected.name }}
                    </h3>
                    <div class="blue--text mb-2">
                      {{ selected.email }}
                    </div>
                  </v-card-text>
                  <v-divider></v-divider>
                  <v-row>
                    <v-col cols="6">
                      Postleitzahl:
                    </v-col>
                    <v-col cols="6">
                      {{ zipCodeObject.zipCode }}
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="6">
                      Stadt:
                    </v-col>
                    <v-col cols="6">
                      {{ zipCodeObject.city }}
                    </v-col>
                  </v-row>
                </v-card>
              </v-scroll-y-transition>
            </v-col>
          </v-row>
        </v-card>
      </v-dialog>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    items: [],
    search: null,
    caseSensitive: false,
    active: [],
    avatar: null,
    open: [],
    users: [],
    dialog: false,
    propId: null,
  }),

  computed: {
    getItems() {
      return this.items;
    },
    filter() {
      return this.caseSensitive
        ? (item, search, textKey) => item[textKey].indexOf(search) > -1
        : undefined;
    },
    ...mapGetters(['isAuthenticated', 'hierarchyMapping']),
    selected() {
      if (!this.active.length) return undefined;
      const id = this.active[0];
      if (!(this.hierarchyMapping.find((user) => user.id === id).level === 5)) return undefined;
      return this.hierarchyMapping.find((user) => user.id === id);
    },
    hierarchyNested() {
      return this.nest(this.hierarchyMapping);
    },
  },

  methods: {
    nest(inputArray) {
      const nested = [];
      inputArray.forEach((item) => { // eslint-disable-line
        var parent = item.parent; // eslint-disable-line
        if (!parent) {
          nested.push(item);
        } else {
          inputArray.forEach((item_2) => { // eslint-disable-line
            if (item_2.id === parent) {
              item_2.children = item_2.children || []; // eslint-disable-line
              if (!(item_2.children.filter((x) => x.id === item.id).length)) {
                item_2.children.push(item);
              }
            }
          });
        }
      });
      return nested;
    },
    show(id) {
      this.dialog = true;
      this.propId = id;
    },
    cancel() {
      this.dialog = false;
    },
    onTakeStammClicked() {
      this.$emit('sendIdToParent', this.active[0]);
      this.dialog = false;
    },
    async loadZipCodeData(id) {
      const url = `${this.API_URL}basic/zip-code/${id}/`;
      const response = await axios.get(url);
      return response.data;
    },
  },
  asyncComputed: {
    zipCodeObject() {
      if (this.active && this.active.length) {
        if (!this.active.length) return undefined;
        const id = this.active[0];
        if (!(this.hierarchyMapping.find((user) => user.id === id).level === 5)) return undefined;
        const zipCodeId = this.hierarchyMapping.find((user) => user.id === id).zipCode;
        return this.loadZipCodeData(zipCodeId);
      }
      return [];
    },
  },
};
</script>

<style></style>
