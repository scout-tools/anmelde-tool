<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="closeDialog">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Excel Datei importieren</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-sheet class="ma-5">
        <v-header>
          Lade hier deine Excel Datei hoch, um dir die manuelle Eingabe zu erleichtern.
        </v-header>
        <v-card class="ma-4 pa-3">
        <input type="file" @change="onFileChange" />
        </v-card>
        <v-card class="ma-4">
          <v-simple-table dense>
            <template v-slot:default>
              <thead>
                <tr>
                  <th
                    class="text-left"
                    v-for="column in Object.keys(chartData[0])"
                    :key="column[0]"
                  >
                    {{ column }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in chartData" :key="item.name">
                  <td
                    v-for="column in Object.keys(chartData[0])"
                    :key="column[0]"
                  >
                    {{ item[column] }}
                  </td>
                  <td>
                    <v-btn icon @click="fillParticipant(item)">
                      <v-icon> mdi-cloud-upload </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-sheet>
      <create-single-person-dialog ref="createSinglePersonDialog"></create-single-person-dialog>
    </v-card>
  </v-dialog>
</template>

<script>
import XLSX from 'xlsx';
import CreateSinglePersonDialog from '@/views/registration/create/steps/dialog/CreateSinglePersonDialog.vue';

export default {
  components: {
    CreateSinglePersonDialog,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    files: [],
    data: {
      name: '',
      description: '',
      address: '',
      city: '',
      zipCode: '',
    },
    chartDataRows: ['firstname', 'lastname'],
    jsonData: [],
    e1: 1,
    showError: false,
    showSuccess: false,
    timeout: 7000,
    chartOptions: {
      table: {
        title: 'Company Performance',
      },
    },
  }),
  methods: {
    onFileChange(e) {
      this.getJsonFromFile(e).then((data) => {
        this.jsonData = data;
      });
    },
    getJsonFromFile(e) {
      return new Promise((resolve) => {
        const files = e.target.files; // eslint-disable-line
        const f = files[0]; // eslint-disable-line
        const reader = new FileReader(); // eslint-disable-line
        reader.onload = (e3) => {
          const data = new Uint8Array(e3.target.result); // eslint-disable-line
          const workbook = XLSX.read(data, {type: 'array'}); // eslint-disable-line
          const firstWorksheet = workbook.Sheets[workbook.SheetNames[0]];
          const dataExport = XLSX.utils.sheet_to_json(firstWorksheet, {
            range: 0,
            blankRows: false,
          });
          resolve(dataExport);
        };
        reader.readAsArrayBuffer(f);
      });
    },
    onClickOk() {
      this.active = false;
    },
    openDialog() {
      this.active = true;
    },
    closeDialog() {
      this.active = false;
      this.$emit('refresh');
    },
    fillParticipant(input) {
      const newInput = this.map(input);
      this.$refs.createSinglePersonDialog.openDialogEdit(newInput);
    },
    map(input) {
      const dto = {
        firstName: '',
        lastName: '',
        street: '',
        zipCode: '',
        phoneNumber: '',
        age: null,
        registration: null,
        eatHabitType: [],
        scoutGroup: null,
        isGroupLeader: false,
        roles: ['1'],
        id: 0,
        zipCodeId: 0,
      };
      dto.firstName = input.Vorname;
      dto.lastName = input.Nachname;
      dto.street = input.Adresse;
      dto.zipCode = input.Postleitzahl;
      dto.phoneNumber = input.Telefonnummer;
      dto.age = input.Alter;
      dto.scoutGroup = input.scoutGroup;
      dto.isGroupLeader = false;
      if (input.Vegetarisch === 'x') {
        dto.eatHabitType.push('Kein Fleisch(vegetarisch)');
      }
      return dto;
    },
  },
  computed: {
    chartData() {
      return this.jsonData;
    },
  },
};
</script>

<style>
</style>
