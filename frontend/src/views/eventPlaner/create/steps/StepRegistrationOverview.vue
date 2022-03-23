<template>
  <v-form ref="StepEventRegistrationModules" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Jetzt geht es ans Eingemachte. Hier bestimmst du den Ablauf und die
          Inhalte einer Registrierung. Es gibt eine Liste an Standard Modulen
          die du hinzufügen kannst, du kannst aber auch selber Module
          definieren. Anhand deiner vorherigen Antworten wurden ein paar Module
          vorselektiert und sind verpflichtend.
        </span>
      </v-row>

      <v-container fluid justify-center class="pa-0">
        <v-flex class="elevation-1 pa-3 ma-2">
          <v-toolbar class="mb-2" color="primary" dark>
            <v-toolbar-title>Registrierungsmodule</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-menu offset-y bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn text fab dark v-bind="attrs" v-on="on">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(item, index) in availableModules"
                  :key="index"
                  @click="addModule(item.id)"
                >
                  <v-list-item-title>{{ item.header }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-toolbar>
          <v-list two-line>
            <v-subheader>
              Die Reihenfolge kann per Drag and Drop geändert werden.
            </v-subheader>
            <draggable
              v-model="items"
              @change="onChanged"
            >
              <template v-for="(moduleMapper, index) in items">
                <v-list-item :key="moduleMapper.id">
                  <v-list-item-avatar color="grey">
                    <span>{{ index + 1 }}</span>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title v-html="moduleMapper.module.header" />
                    <v-list-item-subtitle
                      v-html="moduleMapper.module.description"
                    />
                  </v-list-item-content>
                  <v-list-item-action v-if="editing && !moduleMapper.required">
                    <v-btn @click="removeModule(moduleMapper.id)" icon>
                      <v-icon color="error">mdi-minus</v-icon>
                    </v-btn>
                  </v-list-item-action>
                  <v-list-item-action v-if="editing">
                    <v-btn icon @click="editModule(moduleMapper)">
                      <v-icon color="primary">mdi-pencil</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </draggable>
          </v-list>
        </v-flex>
      </v-container>

      <create-event-registration-module
        ref="newEventDialog"
        @close="onDialogClosed"
      />

      <v-divider class="my-3" />

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submit="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import draggable from 'vuedraggable';
import { orderBy } from 'lodash';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import CreateEventRegistrationModule from '@/components/dialog/CreateEventRegistrationModule.vue';

export default {
  name: 'StepRegistrationOverview',
  header: 'Registrierungsübersicht',
  props: ['position', 'maxPos'],
  components: {
    CreateEventRegistrationModule,
    PrevNextButton,
    draggable,
  },
  mixins: [stepMixin, apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    before: null,
    editing: true,
    availableModules: [],
    items: [],
  }),
  computed: {
  },
  methods: {
    updateData() {},
    removeModule(mapperId) {
      this.deleteEventModule(mapperId)
        .then((success) => {
          console.log(success);
          this.gatherAvailableEventModules();
          this.gatherAssignedEventModules();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    onChanged() {
      console.log(this.items);
      this.items.forEach((item, index) => {
        this.items[index].ordering = index;
      });
      console.log(this.items);

      const promises = [];
      this.items.forEach((item) => {
        console.log(item);
        promises.push(
          this.updateEventModule(
            {
              ordering: item.ordering,
              event: item.event,
              module: item.module.id,
            },
            item.id,
          ),
        );
      });
      Promise.all(promises).then(() => {
        console.log(promises);
      });
    },
    onDialogClosed() {},
    editModule(moduleMapper) {
      this.$refs.newEventDialog.openDialogEdit(moduleMapper);
    },
    addModule(moduleId) {
      const data = {
        event: this.event.id,
        module: moduleId,
      };
      this.addEventModule(data)
        .then(() => {
          this.gatherAvailableEventModules();
          this.gatherAssignedEventModules();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    gatherAvailableEventModules() {
      this.getAvailableEventModules(this.event.id)
        .then((success) => {
          this.availableModules = success.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    gatherAssignedEventModules() {
      this.getAssignedEventModules(this.event.id)
        .then((success) => {
          this.items = orderBy(success.data, 'ordering');
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.gatherAvailableEventModules();
    this.gatherAssignedEventModules();
  },
};
</script>
