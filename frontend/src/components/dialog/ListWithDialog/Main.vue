<template>
  <v-container>
    <v-btn class="ma-2" color="success" @click="newItem">
      <v-icon left> mdi-plus</v-icon>
      Eintrag hinzufügen
    </v-btn>
    <v-btn
      v-if="dialogMeta.excelUpload"
      class="ma-2"
      @click="openExcelDialog"

    >
      <v-icon color="#008000" left> mdi-microsoft-excel</v-icon>
      Excel Datei hochladen
    </v-btn>
    <v-btn
      v-if="dialogMeta.groupAdd"
      class="ma-2"
      @click="openGroupDialog"

    >
      <v-icon color="#008000" left> mdi-account-group</v-icon>
      Gruppe hinzufügen
    </v-btn>
    <v-list v-if="!isLoading">
      <v-subheader>Einträge ({{ items.length || 0 }})</v-subheader>
      <v-list-item-group color="primary" :value="value"
                         @change="onInputChanged">
        <v-list-item v-for="(item, i) in items" :key="i">
          <v-list-item-avatar>
            <v-icon color="black" dark>mdi-account</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              v-text="getDisplayName(item)"
            ></v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn dense icon @click="editParticipant(item)">
              <v-icon color="primary lighten-1">mdi-pencil</v-icon>
            </v-btn>
          </v-list-item-action>
          <v-list-item-action>
            <v-btn dense icon @click="deleteParticipant(item.id)">
              <v-icon color="red lighten-1">mdi-trash-can</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-list-item v-if="!items.length">
          Kein Eintrag vorhanden.
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <v-row align="center" justify="center" class="ma-2">
      <p class="red-text" v-if="getValidationErrorMessage"> {{ getValidationErrorMessage }} </p>
    </v-row>
    <v-row v-if="isLoading">
      <Circual/>
      <v-btn color="success" @click="beforeTabShow">Daten laden</v-btn>
    </v-row>
    <create-modal
      ref="createModal"
      :dialogMeta="dialogMeta"
      @refresh="onRefresh()"
      :valdiationObj="valdiationObj"
      @validate="validate"
    />
    <create-group-modal
      ref="groupDialog"
      :dialogMeta="dialogMeta"
      @refresh="onRefresh()"
      :currentRegistration="currentRegistration"
      :valdiationObj="valdiationObj"
      @validate="validate"
    />
    <delete-modal
      ref="deleteModal"
      :dialogMeta="dialogMeta"
      @refresh="onRefresh()"
    />
    <UploadExcelFile
      ref="uploadExcelFile"
      :dialogMeta="dialogMeta"
      :valdiationObj="valdiationObj"
      @refresh="onRefresh()"
      @validate="validate"
      :currentEvent="currentEvent"
    />
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
import Circual from '@/components/loading/Circual.vue';
import CreateModal from '@/components/dialog/ListWithDialog/CreateModal.vue';
import CreateGroupModal from '@/components/dialog/ListWithDialog/CreateGroupModal.vue';
import DeleteModal from '@/components/dialog/ListWithDialog/DeleteModal.vue';
import UploadExcelFile from './ExcelImport.vue';

export default {
  mixins: [apiCallsMixin],
  components: {
    CreateModal,
    CreateGroupModal,
    UploadExcelFile,
    DeleteModal,
    Circual,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    items: [],
  }),
  props: {
    value: {
      default: null,
    },
    valdiationObj: {},
    dialogMeta: {
      default: {},
    },
    currentRegistration: {
      default: {},
    },
    currentEvent: {
      type: Object,
      default: () => ({}),
    },
  },
  computed: {
    isDev() {
      return process.env.VUE_APP_ENV === 'DEV';
    },
    regId() {
      return this.$route.params.id;
    },
    getValidationErrorMessage() {
      if (this.dialogMeta.minItems && this.dialogMeta.minItems > this.items.length) {
        return `Mindestanzahl: ${this.dialogMeta.minItems}.`;
      }
      if (this.dialogMeta.maxItems && this.dialogMeta.maxItems < this.items.length) {
        return `Maximalanzahl: ${this.dialogMeta.maxItems}.`;
      }
      return null;
    },
  },
  methods: {
    onInputChanged(value) {
      this.$emit('input', value);
    },
    validate(data) {
      this.$emit('validate', data);
    },
    getDisplayName(item) {
      let template = '';
      this.dialogMeta.listDisplay.forEach((field, i) => {
        if (i === 0) {
          template += ` ${item[field]}`;
        } else {
          template += ` - ${item[field]}`;
        }
      });
      return template;
    },
    isValid() {
      return this.getValidationErrorMessage === null;
    },
    getItems() {
      this.isLoading = true;
      Promise.all([this.getService(this.dialogMeta.path)])
        .then((values) => {
          this.items = values[0].data;
          if (this.dialogMeta.orderBy) {
            this.items.sort((a, b) => a[this.dialogMeta.orderBy].localeCompare(b[this.dialogMeta.orderBy])); // eslint-disable-line
          }
          this.isLoading = false;
        })
        .catch((error) => {
          this.$root.globalSnackbar.show({
            message: error.response.data.message,
            color: 'error',
          });
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    editParticipant(item) {
      this.$refs.createModal.openDialogEdit(item);
    },
    deleteSleepingLocation(id) {
      this.deleteEventBookingOption(this.$route.params.id, id)
        .then(() => {
          this.collectBookingOptionss();
        });
    },
    newItem() {
      this.$refs.createModal.openDialog();
    },
    onRefresh() {
      this.getItems();
      this.$emit('refresh');
    },
    openExcelDialog() {
      this.$refs.uploadExcelFile.openDialog();
    },
    openGroupDialog() {
      this.$refs.groupDialog.openDialog();
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

<style>
.red-text {
  color: red !important;
}
</style>
