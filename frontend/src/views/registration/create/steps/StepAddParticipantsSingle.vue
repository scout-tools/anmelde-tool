<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="pa-5">
      <p>
        Bitte trag hier die Daten jede_r einzelnen Teilnehmer_in <b>einzeln</b> ein. <br />
        <br />
        Du hast auch die Möglichkeit die Felder mit Hilfe einer Excel Tabelle
        vorauszufüllen.
      </p>
      <v-btn class="ma-2" color="success" @click="newUser">
        <v-icon left> mdi-plus </v-icon>
        Teilnehmer_in hinzufügen
      </v-btn>
      <v-btn class="ma-2" color="primary" @click="openExcelDialog">
        <v-icon left> mdi-plus </v-icon>
        Excel Datei hochladen
      </v-btn>
      <v-list v-if="!isLoading">
        <v-subheader>Teilnehmer_innen</v-subheader>
        <v-list-item-group color="primary">
          <v-list-item
            v-for="(item, i) in items[0].participantpersonalSet"
            :key="i"
          >
            <v-list-item-avatar>
              <v-icon color="black" dark>mdi-account</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                v-text="item.scoutGroup + ' - ' + item.firstName"
              ></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn dense icon @click="editParticipant(item.id)">
                <v-icon color="primary lighten-1">mdi-pencil</v-icon>
              </v-btn>
            </v-list-item-action>
            <v-list-item-action>
              <v-btn dense icon @click="deleteParticipant(item.id)">
                <v-icon color="red lighten-1">mdi-trash-can</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <div v-else>
        <div class="text-center ma-5">
        <p>
          Lade Daten
        </p>
          <v-progress-circular
            :size="80"
            :width="10"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>
      </div>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-single-person-dialog
      ref="createSinglePersonDialog"
      @refresh="onRefresh()"
    />
    <upload-excel-file
      ref="uploadExcelFile"
      @refresh="onRefresh()"
    />
    <delete-modal
      ref="deleteModal"
      @refresh="onRefresh()"
    />
  </v-form>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

import DeleteModal from '@/views/registration/create/steps/dialog/DeleteModal.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import CreateSinglePersonDialog from './dialog/CreateSinglePersonDialog.vue';
import UploadExcelFile from './dialog/UploadExcelFile.vue';

export default {
  name: 'StepAddParticipantsSingle',
  displayName: 'Teilnehmende',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    PrevNextButtons,
    CreateSinglePersonDialog,
    UploadExcelFile,
    DeleteModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    selectedItem: 1,
    items: [{ participants: [] }],
  }),
  validations: {},
  computed: {
    ...mapGetters([
      'isAuthenticated',
      'getJwtData',
      'hierarchyMapping',
      'ageGroupMapping',
    ]),
    total() {
      return Object.values(this.data).reduce(
        (pv, cv) => parseInt(pv, 10) + parseInt(cv, 10),
        0,
      );
    },
    getActiveAgeGroups() {
      if (
        this.ageGroupMapping && // eslint-disable-line
        this.currentEvent && // eslint-disable-line
        this.currentEvent.ageGroups && // eslint-disable-line
        this.currentEvent.ageGroups.length // eslint-disable-line
      ) {
        return this.ageGroupMapping.filter((item) =>
          this.currentEvent.ageGroups.includes(item.id), // eslint-disable-line
        ); // eslint-disable-line
      }
      return [];
    },
  },
  methods: {
    getParticipants() {
      this.isLoading = true;
      Promise.all([this.loadParticipants()])
        .then((values) => {
          [this.items] = values;
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadParticipants() {
      const path = `${this.API_URL}basic/registration/${this.$route.params.id}/participants/?&timestamp=${new Date().getTime()}`;
      const response = await axios.get(path);

      return response.data;
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    addParticipants() {
      const promises = [];
      const registrationId = this.$route.params.id;
      const myUrl = `${this.API_URL}basic/participant-group/`;
      const valueArray = Object.values(this.data);
      Object.keys(this.data).forEach((element, index) => {
        const paramsData = {
          ageGroup: parseInt(element, 10),
          numberOfPersons: parseInt(valueArray[index], 10),
          registration: parseInt(registrationId, 10),
        };
        promises.push(axios.post(myUrl, paramsData));
      });

      Promise.all(promises).then(() => {
        this.$emit('nextStep');
      });
    },
    editParticipant(id) {
      this.$refs.createSinglePersonDialog.openDialogEdit(
        this.items[0].participantpersonalSet.filter((i) => i.id === id)[0],
      );
    },
    onRefresh() {
      this.getParticipants();
    },
    newUser() {
      this.$refs.createSinglePersonDialog.openDialog();
    },
    openExcelDialog() {
      this.$refs.uploadExcelFile.openDialog();
    },
    deleteParticipant(item) {
      this.$refs.deleteModal.show(item);
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
};
</script>
