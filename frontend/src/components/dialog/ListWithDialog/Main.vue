<template>
  <v-container>
    <v-btn class="ma-2" color="success" @click="newItem">
      <v-icon left> mdi-plus </v-icon>
      Eintrag hinzufügen
    </v-btn>
    <!-- <v-btn class="ma-2" color="primary" @click="openExcelDialog">
        <v-icon left> mdi-plus </v-icon>
        Excel Datei hochladen
      </v-btn> -->
    <v-list v-if="!isLoading">
      <v-subheader>Einträge</v-subheader>
      <v-list-item-group color="primary">
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
        <v-list-item v-if="!items.length">
          Kein Eintrag vorhanden.
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <div v-else>
      <Circual/>
    </div>
    <create-modal ref="createModal" :dialogMeta="dialogMeta" @refresh="onRefresh()" />
    <delete-modal ref="deleteModal" :dialogMeta="dialogMeta" @refresh="onRefresh()" />
  </v-container>
</template>

<script>
import CreateModal from '@/components/dialog/ListWithDialog/CreateModal.vue';
import DeleteModal from '@/components/dialog/ListWithDialog/DeleteModal.vue';
import Circual from '@/components/loading/Circual.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  components: {
    CreateModal,
    DeleteModal,
    Circual,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    selectedItem: 1,
    items: [],
  }),
  props: {
    dialogMeta: {
      default: {},
    },
  },
  validations: {},
  computed: {
    regId() {
      return this.$route.params.id;
    },
  },
  methods: {
    getDisplayName(item) {
      const returnString = `${item.firstName} -  ${item.lastName}`;
      return returnString;
    },
    getItems() {
      this.isLoading = true;
      Promise.all([this.getRegService('single-participant', this.regId)])
        .then((values) => {
          this.items = values[0].data;
          this.isLoading = false;
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    editParticipant(id) {
      this.$refs.createModal.openDialogEdit(id);
    },
    deleteSleepingLocation(id) {
      this.deleteEventBookingOption(this.$route.params.id, id).then(() => {
        this.collectBookingOptionss();
      });
    },
    newItem() {
      this.$refs.createModal.openDialog();
    },
    onRefresh() {
      this.getItems();
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

<style>
</style>
