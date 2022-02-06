<template>
  <v-form ref="StepVisibility" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
         Jetzt geht es ans eingemacht.
          Hier bestimmst du den Ablauf und die Inhalte einer Registrierung.
          Es gibt eine Liste an Standard Elementen die du hinzufügen kannst, du kannst aber auch
          selber elemente definieren.
        </span>
      </v-row>

      <v-container fluid justify-center>
        <v-flex class="elevation-1 pa-3 ma-2">
          <v-toolbar class="mb-2" color="primary" dark>
            <v-toolbar-title>Registrierungsmodule</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn>
              Modul hinzufügen
            </v-btn>
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
            <draggable :disabled="!this.editing" v-model="items" >
              <template v-for="(moduleMapper, index) in items">
                <v-list-item :key="moduleMapper.ID">
                  <v-list-item-avatar color="grey">
                    <span>{{ index + 1 }}</span>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title v-html="moduleMapper.Title"/>
                    <v-list-item-subtitle v-html="moduleMapper.Description"/>
                  </v-list-item-content>
                  <v-list-item-action v-if="editing">
                    <v-btn @click="remove(index)" icon>
                      <v-icon>mdi-close</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </template>
            </draggable>
          </v-list>
        </v-flex>
      </v-container>

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
import stepMixin from '@/mixins/stepMixin';
// import store from '@/store';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';

export default {
  name: 'StepRegistrationOverview',
  header: 'Registrierungsübersicht',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
    draggable,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    before: null,
    editing: false,
    itemsExample: [
      {
        ID: 1,
        Title: 'Fact sheets, brochures, educational materials',
        Ordering: 1,
        Subtitle: '',
      },
      {
        ID: 2,
        Title: 'HHS Clearance submission',
        Ordering: 2,
        Subtitle: '(for campaigns, campaign products, and/or videos)',
      },
      {
        ID: 3,
        Title: 'Abstracts',
        Ordering: 3,
        Subtitle: '',
      },
      {
        ID: 4,
        Title: 'Non-media Blog/blog posts',
        Ordering: 4,
        Subtitle: '(internal or external)',
      },
      {
        ID: 5,
        Title: 'CDC Connects articles',
        Ordering: 5,
        Subtitle: '',
      },
      {
        ID: 6,
        Title: 'CDC.gov features',
        Ordering: 6,
        Subtitle: '',
      },
      {
        ID: 7,
        Title: 'Logo use/branding',
        Ordering: 7,
        Subtitle: '',
      },
      {
        ID: 8,
        Title: 'External newsletters',
        Ordering: 8,
        Subtitle: '',
      },
      {
        ID: 9,
        Title: 'Infographics',
        Ordering: 9,
        Subtitle: '',
      },
      {
        ID: 10,
        Title: 'Other',
        Ordering: 10,
        Subtitle: '',
      }],
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
  },
  mounted() {
    this.items = [];
    this.event.eventmodulemapperSet.forEach((item) => {
      const data = {
        ID: item.id,
        Title: item.module.header,
        order: item.ordering,
        Subtitle: item.module.description,
      };
      console.log(data);
      this.items.push(data);
    });
  },
};
</script>
