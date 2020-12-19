<template>
<v-container>
  <v-row justify="center">
    <v-dialog v-model="dialog" transition="dialog-top-transition"
    persistent max-width="600px">
  <v-card
    class="mx-auto"
    width="800"
  >
    <v-card-title class="primary white--text headline">
      Stämme
    </v-card-title>
    <v-row
      class="pa-4"
      justify="space-between"
    >
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
          :items="herarchyNested"
          :open.sync="open"
          activatable
          :search="search"
          color="warning"
          open-on-click
          transition
        >
          <template v-slot:prepend="{ item }">
            <v-icon v-if="!item.children">
              mdi-account-group
            </v-icon>
            <v-icon v-else>
              mdi-family-tree
            </v-icon>
          </template>
        </v-treeview>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col
        class="d-flex text-center"
      >
        <v-scroll-y-transition mode="out-in">
          <div
            v-if="!selected"
            class="title grey--text text--lighten-1 font-weight-light"
            style="align-self: center;"
          >
            Wähle einen Stamm
          </div>
          <v-card
            v-else
            :key="selected.id"
            class="pt-6 mx-auto"
            flat
            max-width="400"
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
            <v-row
              class="text-left"
              tag="v-card-text"
            >
              <v-col
                class="text-right mr-4 mb-2"
                tag="strong"
                cols="5"
              >
                Postleitzahl:
              </v-col>
              <v-col>
                {{ selected.zipCode }}
              </v-col>
            </v-row>
          </v-card>
        </v-scroll-y-transition>
      </v-col>
    </v-row>
    <v-card-actions>

      <v-spacer></v-spacer>

      <v-btn
        :disabled="!selected"
        class="white--text"
        color="green darken-1"
        depressed
        @click="onTakeStammClicked"
      >
        Diesen Stamm übernehmen
        <v-icon right>
          mdi-content-save
        </v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
    </v-dialog>
  </v-row>
</v-container>
</template>

<script>
// import axios from 'axios';
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
    ...mapGetters([
      'isAuthenticated',
      'herarchy',
    ]),
    selected() {
      if (!this.active.length) return undefined;
      // if (this.propId && this.propId === this.active[0]) {
      //   return this.herarchy.find((user) => user.id === this.propId);
      // }
      const id = this.active[0];
      if (!(this.herarchy.find((user) => user.id === id).level === 5)) return undefined;
      return this.herarchy.find((user) => user.id === id);
    },
    herarchyNested() {
      return this.nest(this.herarchy);
    },
  },

  methods: {
    nest(array) {
      const nested = [];
      for (let i = 0; i < array.length; i++) { // eslint-disable-line
        var parent = array[i].parent; // eslint-disable-line
        if (!parent) {
          nested.push(array[i]);
        } else {
          // You'll want to replace this with a more efficient search
          for (let j = 0; j < array.length; j++) { // eslint-disable-line
            if (array[j].id === parent) {
              array[j].children = array[j].children || []; // eslint-disable-line
              array[j].children.push(array[i]);
              break;
            }
          }
        }
      }
      return nested;
    },
    show(id) {
      this.dialog = true;
      this.propId = id;
    },
    cancel() {
      this.dialog = false;
      this.$emit('dialogClose');
    },
    onTakeStammClicked() {
      this.$emit('sendIdToParent', this.active[0]);
      this.dialog = false;
    },
  },
};
</script>

<style>

</style>
