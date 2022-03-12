<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="pa-5 my-5">
      <p>
        Ich melde folgende Teilnehmende an <br />
        <br />
        Die Erfassung erfolgt pro Person. <br />
        <br />
        Alternativ kannst du hier die Excelliste hochladen, wenn du die Daten
        dort bereits erfasst hast.
        <br />
        <a
          target="_blank"
          href="https://cloud.dpvonline.de/s/fMMrgfpf5dAm9Fg"
          style="color: blue"
        >
          Link zur Beispiel Excel Datei
        </a>
      </p>
      <v-btn class="ma-2" color="success" @click="newUser">
        <v-icon left> mdi-plus </v-icon>
        Neu
      </v-btn>
      <!-- <v-btn class="ma-2" color="primary" @click="openExcelDialog">
        <v-icon left> mdi-plus </v-icon>
        Excel Datei hochladen
      </v-btn> -->
      <v-list v-if="!isLoading">
        <v-subheader>Teilnehmer_innen</v-subheader>
        <v-list-item-group color="primary">
          <v-list-item v-for="(item, i) in sleepingLocations" :key="i">
            <v-list-item-avatar>
              <v-icon color="black" dark>mdi-account</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                v-text="getDisplayName(item)"
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
          <v-list-item v-if="!sleepingLocations.length">
            Bisher hast du noch niemanden hinzugefügt.
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <div v-else>
        <div class="text-center ma-5">
          <p>Lade Daten</p>
          <v-progress-circular
            :size="80"
            :width="10"
            color="primary"
            indeterminate
          ></v-progress-circular>
        </div>
      </div>
      <v-divider class="my-3" />
      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <!-- <create-single-person-dialog
      ref="createSinglePersonDialog"
      @refresh="onRefresh()"
    />
    <upload-excel-file ref="uploadExcelFile" @refresh="onRefresh()" /> -->
    <delete-modal ref="deleteModal" @refresh="onRefresh()" />
  </v-form>
</template>

<script>
import axios from 'axios';

import DeleteModal from '@/components/dialog/DeleteModal.vue';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
// import CreateSinglePersonDialog from '../dialog/CreateSinglePersonDialogBundesfahrt.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  name: 'StepParticipationFeeComplex',
  header: 'Teilnehmer_innen Beitrag',
  props: ['position', 'maxPos'],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    PrevNextButton,
    DeleteModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    selectedItem: 1,
    items: [{ participants: [] }],
    sleepingLocations: [],
  }),
  validations: {},
  computed: {
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
        return this.ageGroupMapping.filter(
          (item) => this.currentEvent.ageGroups.includes(item.id), // eslint-disable-line
        ); // eslint-disable-line
      }
      return [];
    },
  },
  methods: {
    getDisplayName(item) {
      const returnString = `${item.name} -  ${item.price} €`;
      return returnString;
    },
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
      const path = `${this.API_URL}basic/registration/${
        this.$route.params.id
      }/participants/?&timestamp=${new Date().getTime()}`;
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
    editParticipant(id) {
      this.$refs.createSinglePersonDialog.openDialogEdit(
        this.items[0].participantpersonalSet.filter((i) => i.id === id)[0],
      );
    },
    collectSleepingLocations() {
      this.isLoading = true;
      // this.getEventSleepingLocation(this.$route.params.id)
      //   .then((success) => {
      //     this.sleepingLocations = success.data;
      //     this.isLoading = false;
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //   });
    },
    deleteSleepingLocation(id) {
      this.deleteEventBookingOption(this.$route.params.id, id)
        .then(() => {
          this.collectBookingOptionss();
        });
    },
    newUser() {
      this.$refs.createSinglePersonDialog.openDialog();
    },
    onRefresh() {
      this.collectSleepingLocations();
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
