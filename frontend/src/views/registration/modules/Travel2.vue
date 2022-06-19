<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :loading="isLoading"
    :saving="saving"
    :position="position"
    :maxPos="maxPos"
    :currentMod="currentModule"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
    @saving="onSaving"
  >
    <template v-slot:header>
      <p>Bitte trage hier ein wann und wie deine Gruppe zur Veranstaltung anreisen werdet.
        Du kannst dazu alle Personen auf einmal eintragen oder deine Teilnehmenden aufteilen.
        Bitte achte darauf, dass am Ende alle deine Teilnehmeden aufteilt sind.</p>
    </template>

    <template v-slot:main>
  <v-container>
    <v-row v-if="!isLoading">
      <v-spacer></v-spacer>
    <v-btn class="ma-2" color="success" @click="newItem">
      <v-icon left> mdi-plus</v-icon>
      Anreise hinzufügen
    </v-btn>
    <v-btn v-if="selectedItem && selectedItem.id" class="ma-2" color="primary"
      @click="editParticipant(selectedItem)">
      <v-icon >mdi-pencil</v-icon>
      Editieren
    </v-btn>
    <v-btn v-if="selectedItem && selectedItem.id" class="ma-2" color="error"
      @click="deleteParticipant(selectedItem.id)">
      <v-icon >mdi-trash-can</v-icon>
      Löschen
    </v-btn>
    </v-row>
    <v-row align="center" justify="center" v-show="!isLoading">
      <List
        :key="`travelist${items.length}`"
        v-if="!isLoading"
        ref="travelListItems"
        :items="getTravel2Items()"
        :summaryData="summaryData" :item="item"
        @onItemChanged="onItemChanged"/>
    </v-row >
    <v-row align="center" justify="center" class="ma-2" v-if="!isLoading">
      <p class="red-text" v-if="getValidationErrorMessage"> {{ getValidationErrorMessage }} </p>
    </v-row>
    <v-row align="center" justify="center" v-if="isLoading">
      <Circual/>
    </v-row>
    <v-row align="center" justify="center" v-if="isLoading" class="ma-4">
      <v-btn color="success" @click="beforeTabShow">Daten laden</v-btn>
    </v-row>
    <create-modal
      ref="createModal"
      :dialogMeta="dialogMeta"
      :currentEvent="currentEvent"
      :currentRegistration="currentRegistration"
      :currentModule="currentModule"
      :moduleData="moduleData"
      @refresh="onRefresh()"
      :valdiationObj="$v"
      @validate="validate"

    />
    <delete-modal
      ref="deleteModal"
      :dialogMeta="dialogMeta"
      @refresh="onRefresh()"
    />
  </v-container>
    </template>
  </GenericRegModul>
</template>

<script>
import axios from 'axios';

import Circual from '@/components/loading/Circual.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import { mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';

import CreateModal from './travel2/CreateModal.vue';
import DeleteModal from './travel2/DeleteModal.vue';
import List from './travel2/List.vue';

export default {
  name: 'StepConsent',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'currentModule',
    'personalData',
  ],
  components: {
    GenericRegModul,
    CreateModal,
    DeleteModal,
    Circual,
    List,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    saving: false,
    isLoading: true,
    moduleData: [],
    attributes: [],
    participantCount: 0,
    item: null,
    selectedItem: {},
    data: {
      vehicle: '',
      time: '',
    },
  }),
  validations: {
    data: {
      typeField: {
        required,
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    moduleId() {
      return this.currentModule.module.id;
    },
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
    },
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: true,
        listDisplay: ['firstName', 'lastName'],
        orderBy: 'firstName',
        maxItems: null,
        minItems: 1,
        path: this.path,
        fields: [
          {
            name: 'Verkehrsmittel*',
            techName: 'typeField',
            tooltip: 'Mit welchem Verkehrsmittel werdet ihr anreisen?',
            icon: 'mdi-train-car',
            mandatory: true,
            lookupPath: '/basic/travel-type-choices/',
            lookupListDisplay: ['name'],
            fieldType: 'enumCombo',
            multiple: false,
            default: 'T',
          },
          {
            name: 'Zeipunkt*',
            techName: 'dateTimeField',
            tooltip: 'Zu welchem Zeitpunkt werdet ihr ungefährt ankommen?',
            icon: 'mdi-clock',
            mandatory: true,
            fieldType: 'datetime',
            multiple: false,
            default: this.currentEvent.startDate,
          },
          {
            name: 'Anzahl der reisenden Personen',
            techName: 'numberPersons',
            tooltip: 'Wieviele Personen reisen gemeinsam?',
            icon: 'mdi-clock',
            mandatory: true,
            fieldType: 'number',
            default: this.participantCount,
          },
          {
            name: 'Zusatzinfos (Bahnhof, Parkplatz, Abholwunsch, Verspätungsgrund)',
            techName: 'description',
            tooltip: 'Geb hier Informationen zu euren Reise an, die für das Planungsteam wichtig sein könnte. ',
            icon: 'mdi-pencil',
            mandatory: true,
            fieldType: 'textarea',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    getTravel2Items() {
      return this.items.filter(
        (item) => item.resourcetype === 'TravelAttributeV2',
      );
    },
    onItemChanged(item) {
      this.item = item;
      this.selectedItem = this.getTravel2Items()[item];
    },
    setDefaults() {
      this.moduleData.forEach((item) => {
        if (item && item.attribute.resourcetype === 'TravelAttribute') {
          this.data.vehicle = this.getAttributeValue(item)[0]; //eslint-disable-line
          this.data.time = this.getAttributeValue(item)[1]; //eslint-disable-line
        }
      });
      this.$forceUpdate();
    },
    getAttributeValue(item) {
      const value = this.attributes.filter(
        (att) => att.templateId === item.attribute.id,
      );
      if (value && value.length) {
        return [value[0].typeField, value[0].timeField];
      }
      return [null, null];
    },
    validate(data) {
      this.data = data;
      this.$v.$touch();
    },
    onNextStep() {
      this.saving = true;
      this.validate();
      if (!this.valid) {
        this.saving = false;
        return;
      }
      this.$emit('nextStep');
    },
    editParticipant(item) {
      this.$refs.createModal.openDialogEdit(item);
    },
    newItem() {
      this.$refs.createModal.openDialog();
    },
    onRefresh() {
      this.isLoading = true;
      setTimeout(() => this.loadData(), 100);
    },
    deleteParticipant(item) {
      this.$refs.deleteModal.show(item);
    },
    beforeTabShow() {
      this.onRefresh();
    },
    loadData() {
      this.isLoading = true;
      this.saving = false;
      Promise.all([
        axios.get(`${process.env.VUE_APP_API}/${this.path}`),
        this.getRegService('summary', this.currentRegistration.id),
        this.getModule(this.currentModule.id, this.currentEvent.id),
      ])
        .then((values) => {
          this.items = values[0].data;
          this.summaryData = values[1].data[0]; //eslint-disable-line
          this.moduleData = values[2].data; //eslint-disable-line
          this.participantCount = values[1].data[0].participantCount; //eslint-disable-line
          this.isLoading = false;
          this.$forceUpdate();
        })
        .catch((error) => {
          console.log(error);
          // this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
