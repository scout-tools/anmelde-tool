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
    <v-list>
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
    <create-modal
      :dialogMeta="dialogMeta"
      ref="createModal"
      @refresh="onRefresh()"
    />
    <delete-modal
      :dialogMeta="dialogMeta"
      ref="deleteModal"
      @refresh="onRefresh()"
    />
  </v-container>
</template>

<script>
import CreateModal from '@/components/dialog/ListWithDialog/CreateModal.vue';
import DeleteModal from '@/components/dialog/ListWithDialog/DeleteModal.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  components: {
    CreateModal,
    DeleteModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isLoading: true,
    selectedItem: 1,
  }),
  props: {
    items: {
      default: {},
    },
  },
  validations: {},
  computed: {
    regId() {
      return this.$route.params.id;
    },
    dialogMeta() {
      return {
        path: `event/registration/${this.regId}/attribute`,
        fields: [
          {
            name: 'Name*',
            techName: 'name',
            tooltip: '',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Beschreibung*',
            techName: 'description',
            tooltip: '',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Preis*',
            techName: 'price',
            tooltip: '',
            mandatory: true,
            fieldType: 'currency',
            default: '',
          },
        ],
      };
    },
  },
  methods: {
    getDisplayName(item) {
      // const template = '';
      // this.dialogMeta.listDisplay.forEach((field, i) => {
      //   if (i === 0) {
      //     template += ` ${item[field]}`;
      //   } else {
      //     template += ` - ${item[field]}`;
      //   }
      // });
      return item.title;
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
