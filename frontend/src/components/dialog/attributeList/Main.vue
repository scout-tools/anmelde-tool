<template>
  <v-container>
    <v-btn disabled class="ma-2" color="success" @click="newItem">
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
            <v-btn disabled dense icon @click="editParticipant(item.id)">
              <v-icon color="primary lighten-1">mdi-pencil</v-icon>
            </v-btn>
          </v-list-item-action>
          <v-list-item-action>
            <v-btn disabled dense icon @click="deleteParticipant(item.id)">
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
      :moduleMapper="moduleMapper"
      ref="createModalAttribute"
      @refresh="onRefresh()"
      :valdiationObj="$v"
    />
    <delete-modal
      :dialogMeta="dialogMeta"
      :moduleMapper="moduleMapper"
      ref="deleteModalAttribute"
      @refresh="onRefresh()"
      :valdiationObj="$v"
    />
  </v-container>
</template>

<script>
import CreateModal from '@/components/dialog/attributeList/CreateModal.vue';
import DeleteModal from '@/components/dialog/attributeList/DeleteModal.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import { required } from 'vuelidate/lib/validators';

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
    moduleMapper: {
      default: {},
    },
  },
  validations: {
    data: {
      title: {
        required,
      },
      text: {
        required,
      },
    },
  },
  computed: {
    regId() {
      return this.$route.params.id;
    },
    dialogMeta() {
      return {
        path: `event/registration/${this.regId}/attribute`,
        regId: this.regId,
        fields: [
          {
            name: 'Titel',
            techName: 'title',
            tooltip: '',
            mandatory: true,
            fieldType: 'textfield',
            default: '',
          },
          {
            name: 'Text',
            techName: 'text',
            tooltip: '',
            mandatory: true,
            fieldType: 'textarea',
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
      this.$refs.createModalAttribute.openDialogEdit(id);
    },
    deleteSleepingLocation(id) {
      this.deleteEventBookingOption(this.$route.params.id, id).then(() => {
        this.collectBookingOptionss();
      });
    },
    newItem() {
      this.$refs.createModalAttribute.openDialog();
    },
    onRefresh() {
      this.$emit('refresh');
    },
    openExcelDialog() {
      this.$refs.uploadExcelFile.openDialog();
    },
    deleteParticipant(id) {
      this.$refs.deleteModalAttribute.show(id);
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
};
</script>

<style>
</style>
