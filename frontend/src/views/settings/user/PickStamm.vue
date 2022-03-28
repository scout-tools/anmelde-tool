<template>
  <v-container>
    <v-row justify="center">
      <v-dialog
        v-model="dialog"
        transition="dialog-top-transition"
        fullscreen
        hide-overlay>
        <v-card>
          <v-toolbar
            dark
            color="primary">
            <v-btn
              icon
              dark
              @click="cancel">
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
                @click="onTakeStammClicked">
                Das ist mein Stamm
                <v-icon right> mdi-content-save</v-icon>
              </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-card-text>
            <!--<v-icon class="ma-2" color="error">mdi-alert-circle</v-icon>-->
            <br>Du bist kein Mitglied eines Stammes mehr? Wähle einfach deinen Bund aus.
            <br>Dein Stamm fehlt oder der Ort/die Postleitzahl ist falsch?
            <br>Schreibe uns eine E-Mail an:
            <a href="mailto:support@anmelde-tool.de">support@anmelde-tool.de</a>
          </v-card-text>
          <v-row class="ma-2" justify="space-between">
            <v-col cols="5">
              <v-text-field
                v-model="search"
                label="Suche deinen Stamm"
                flat
                clearable
                clear-icon="mdi-close-circle-outline"/>
              <v-treeview
                :active.sync="active"
                :items="hierarchyNested"
                :open.sync="open"
                open-all
                activatable
                :search="search"
                color="warning"
                transition>
              </v-treeview>
            </v-col>

            <v-divider vertical/>

            <v-col class="d-flex text-center">
              <v-scroll-y-transition mode="out-in">
                <div
                  v-if="!selected"
                  class="title grey--text text--lighten-1 font-weight-light">
                  Wähle einen Stamm
                </div>
                <v-card
                  v-else
                  :key="selected.id"
                  min-width="300"
                  class="mx-auto"
                  flat>
                  <v-card-text>
                    <h3 class="headline mb-2">
                      {{ selected.name }}
                    </h3>
                    <div class="blue--text mb-2">
                      {{ selected.email }}
                    </div>
                  </v-card-text>
                  <v-divider/>
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
import basicInfoMixin from '@/mixins/basicInfoMixin';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    search: '',
    active: [],
    open: [],
    dialog: false,
    currentHierachy: {
      id: String,
      name: String,
      parent: String,
      zipCode: String,
    },
    hierarchies: [],
    zipCodeObject: {
      zipCode: '',
      city: '',
    },
  }),
  mixins: [basicInfoMixin],
  computed: {
    selected() {
      if (!this.active.length) return undefined;
      const id = this.active[0];
      return this.hierarchies.find((user) => user.id === id);
    },
    hierarchyNested() {
      return this.nest(this.hierarchies);
    },
  },
  methods: {
    nest(inputArray) {
      const nested = [];
      inputArray.forEach((item) => { // eslint-disable-line
        const parent = item.parent; // eslint-disable-line
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
    show(currentScouthierachy) {
      this.open = [];
      this.active = [];
      this.dialog = true;
      if (currentScouthierachy) {
        this.currentHierachy = currentScouthierachy;
        this.active = [currentScouthierachy.id];
        let iterateHierachy = currentScouthierachy;
        while (iterateHierachy) {
          this.open.push(iterateHierachy.parent);
          const newIterate = this.hierarchies.find((user) => user.id === iterateHierachy.parent);// eslint-disable-line
          iterateHierachy = newIterate;
        }
      }
    },
    cancel() {
      this.dialog = false;
    },
    onTakeStammClicked() {
      if (this.active) {
        const selectedHierachy = this.hierarchies.find((user) => user.id === this.active[0]);
        this.$emit('sendIdToParent', selectedHierachy);
      }
      this.dialog = false;
    },
  },
  async created() {
    const path = `${process.env.VUE_APP_API}/basic/scout-hierarchy/`;
    const response = await axios.get(path);
    this.hierarchies = response.data;
  },
  watch: {
    async active() {
      const undef = {
        zipCode: '',
        city: '',
      };
      if (this.active && this.active.length) {
        const id = this.active[0];
        if (!(this.hierarchies.find((user) => user.id === id).level === 5)) {
          this.zipCodeObject = undef;
          return;
        }
        const zipCodeId = this.hierarchies.find((user) => user.id === id).zipCode;
        this.zipCodeObject = await this.getZipcodeInfo(zipCodeId);
      } else {
        this.zipCodeObject = undef;
      }
    },
  },
};
</script>
