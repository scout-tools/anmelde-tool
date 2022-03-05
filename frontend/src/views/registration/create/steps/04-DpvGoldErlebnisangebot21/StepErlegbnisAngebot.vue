<template>
  <v-form ref="formWorkshop" v-model="valid">
    <v-container class="pa-5 my-5">
      <p>
        Bitte trage hier dein Erlebnisangebot ein. <br />
        <br />
        Falls du Inspirationen oder Ideen brauchst kannst du gerne
        <a
          style="color: blue"
          target="_blank"
          href="https://docs.google.com/document/d/1DoACKvb5GdbcfumOU1vLRAM_JXjA_bcdKblyuxDGCwA/edit?usp=sharing"
          >hier</a
        >
        schauen.
      </p>
      <v-btn class="ma-2" color="secondary" @click="newAG">
        <v-icon left> mdi-plus </v-icon>
        Erlebnisangebot hinzufügen
      </v-btn>
      <v-list v-if="!isLoading">
        <v-subheader>Erlebnisangebote</v-subheader>
        <v-list-item-group color="primary">
          <v-list-item v-for="(item, i) in items[0].workshops" :key="i">
            <v-list-item-avatar>
              <v-icon color="black" dark>mdi-school</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"></v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-btn dense icon @click="editWorkshop(item.id)">
                <v-icon color="primary lighten-1">mdi-pencil</v-icon>
              </v-btn>
            </v-list-item-action>
            <v-list-item-action>
              <v-btn dense icon @click="deleteWorkshop(item.id)">
                <v-icon color="red lighten-1">mdi-trash-can</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-list-item v-if="!items[0].workshops.length">
            Bisher hast du noch kein Erlebnisangebot hinzugefügt.
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
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-single-workshop-dialog
      ref="createSingleWorkshopDialog"
      @refresh="onRefresh()"
    />
    <delete-workshop-modal ref="deleteModal" @refresh="onRefresh()" />
  </v-form>
</template>

<script>
import PrevNextButtons from '@/views/registration/create/components/button/PrevNextButtonsSteps.vue';
import axios from 'axios';
import CreateSingleWorkshopDialog from './dialog/CreateSingleWorkshopDialog.vue';
import DeleteWorkshopModal from './dialog/DeleteWorkshopModal.vue';

export default {
  name: 'StepWorkshop',
  displayName: 'Erlebnisangebot',
  props: ['position', 'maxPos', 'currentEvent'],
  components: {
    DeleteWorkshopModal,
    CreateSingleWorkshopDialog,
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    participantCount: null,
    items: [{ workshops: [] }],
  }),
  computed: {
    workShopCount() {
      const count = this.participantCount;
      if (!count) return null;
      if (count <= 5) return 0;
      return Math.ceil(count / 15);
    },
    workShopCountString() {
      const count = this.participantCount;
      if (!count) return null;
      if (count <= 5) return '0-1';
      return Math.ceil(count / 15);
    },
  },
  methods: {
    async getWorkshops() {
      this.isLoading = true;
      try {
        this.items[0].workshops = await this.loadWorkshops();
        this.participantCount = await this.loadParticipantCount();
      } catch (error) {
        this.errormsg = error.response.data.message;
      }
      this.isLoading = false;
    },
    async loadWorkshops() {
      const path = `${this.API_URL}basic/workshop/?registration=${
        this.$route.params.id
      }&timestamp=${new Date().getTime()}`;
      const response = await axios.get(path);
      return response.data;
    },
    async loadParticipantCount() {
      const path = `${this.API_URL}basic/registration/${
        this.$route.params.id
      }/participants/?&timestamp=${new Date().getTime()}`;
      const { data } = await axios.get(path);
      return data[0].participantpersonalSet.length;
    },
    validate() {
      this.valid = this.workShopCount <= this.items[0].workshops.length;
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
    editWorkshop(id) {
      this.$refs.createSingleWorkshopDialog.openDialogEdit(
        this.items[0].workshops.filter((i) => i.id === id)[0],
      );
    },
    onRefresh() {
      this.getWorkshops();
      this.valid = true;
    },
    newAG() {
      this.$refs.createSingleWorkshopDialog.openDialog();
    },
    deleteWorkshop(item) {
      this.$refs.deleteModal.show(item);
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
};
</script>
