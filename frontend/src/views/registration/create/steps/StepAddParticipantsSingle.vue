<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="pa-5">
      <v-btn class="ma-2" color="success" @click="newUser">
        <v-icon left> mdi-plus </v-icon>
        Teilnehmer_innen hinzufügen
      </v-btn>
      <v-btn class="ma-2" color="primary" @click="openExcelDialog">
        <v-icon left> mdi-plus </v-icon>
        Excel Datei hochladen
      </v-btn>
      <v-list>
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
      @refresh="getParticipants()"
    />
    <upload-excel-file ref="uploadExcelFile" />
    <delete-modal ref="deleteModal" @refresh="onRefresh" />
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
  name: 'StepNameDescription',
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
    isLoading: false,
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
        return this.ageGroupMapping.filter((item) => this.currentEvent.ageGroups.includes(item.id));
      }
      return [];
    },
  },
  created() {
    this.getParticipants();
  },
  methods: {
    getParticipants() {
      axios
        .get(
          `${this.API_URL}basic/registration/${
            this.$route.params.id
          }/participants/?&timestamp=${new Date().getTime()}`,
        )
        .then((res) => {
          this.items = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
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
  },
};
</script>
