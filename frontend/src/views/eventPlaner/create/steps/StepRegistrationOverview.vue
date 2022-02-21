<template>
  <v-form ref="StepVisibility" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Jetzt geht es ans Eingemachte.
          Hier bestimmst du den Ablauf und die Inhalte einer Registrierung.
          Es gibt eine Liste an Standard Modulen die du hinzufügen kannst, du kannst aber auch
          selber Module definieren.
          Anhand deiner vorherigen Antworten wurden ein paar Module vorselektiert
          und sind verpflichtend.
        </span>
      </v-row>

      <v-container fluid justify-center>
        <v-flex class="elevation-1 pa-3 ma-2">
          <v-toolbar class="mb-2" color="primary" dark>
            <v-toolbar-title>Registrierungsmodule</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu offset-y bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  v-bind="attrs"
                  v-on="on">
                  Module hinzufügen
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(item, index) in availableModules"
                  :key="index"
                  @click="addModule">
                  <v-list-item-title>{{ item.header }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-btn icon @click="action('edit')" v-if="!editing">
              <v-icon>sort</v-icon>
            </v-btn>
            <v-btn icon @click="action('done')" v-if="editing">
              <v-icon>done</v-icon>
            </v-btn>
            <v-btn icon @click="action('undo')" v-if="editing">
              <v-icon>close</v-icon>
            </v-btn>
          </v-toolbar>
          <v-list two-line>
            <draggable :disabled="!this.editing"
                       v-model="items"
                       @change="onChanged">
              <template v-for="(moduleMapper, index) in items">
                <v-list-item :key="moduleMapper.id">
                  <v-list-item-avatar color="grey">
                    <span>{{ index + 1 }}</span>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title v-html="moduleMapper.module.header"/>
                    <v-list-item-subtitle v-html="moduleMapper.module.description"/>
                  </v-list-item-content>
                  <v-list-item-action v-if="editing && !moduleMapper.required">
                    <v-btn @click="remove(index)" icon>
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-list-item-action>
                  <v-list-item-action v-if="editing">
                    <v-btn icon @click="editModule(moduleMapper)">
                      <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </draggable>
          </v-list>
        </v-flex>
      </v-container>

      <create-event-registration-module ref="newEventDialog" @close="onDialogClosed"/>

      <v-divider class="my-3"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { mapGetters } from 'vuex';
import draggable from 'vuedraggable';
import { orderBy } from 'lodash';
import stepMixin from '@/mixins/stepMixin';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import CreateEventRegistrationModule from '@/components/dialogs/CreateEventRegistrationModule.vue';
import axios from 'axios';
// import store from '@/store';

export default {
  name: 'StepRegistrationOverview',
  header: 'Registrierungsübersicht',
  props: ['position', 'maxPos'],
  components: {
    CreateEventRegistrationModule,
    PrevNextButton,
    draggable,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    before: null,
    editing: false,
    availableModules: [],
    items: [],
  }),
  computed: {
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
    },
    action(e) {
      if (e === 'edit') this.before = Object.assign([], this.itemsExample);
      if (e === 'undo') this.itemsExample = this.before;
      this.editing = !this.editing;
    },
    remove(i) {
      this.$delete(this.itemsExample, i);
    },
    onChanged(props) {
      console.log(props);
      this.items.forEach((item, index) => {
        this.items[index].ordering = index;
      });
    },
    onDialogClosed() {

    },
    editModule(moduleMapper) {
      console.log(moduleMapper);
      this.$refs.newEventDialog.openDialogEdit(moduleMapper);
    },
    addModule() {

    },
  },
  mounted() {
    this.items = orderBy(this.event.eventmodulemapperSet, 'ordering');
    const urlAvailableModules = `${this.API_URL}/event/event/${this.event.id}/available-modules/`;
    axios.get(urlAvailableModules)
      .then((success) => {
        console.log(success.data);
        this.availableModules = success.data;
      });
  },
};
</script>
