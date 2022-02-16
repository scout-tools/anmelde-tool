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
          Lade hier deine Excel Datei hoch, um dir die manuelle Eingabe zu
          erleichtern. Die Datei muss in einem bestimmten Format sein.
          <a target="_blank" style="color:blue;" href="https://cloud.dpvonline.de/s/fMMrgfpf5dAm9Fg"
            >Link zur DPV-Cloud</a
          >
        </v-header>
        <v-card class="ma-4 pa-3">
          <input type="file" @change="onFileChange" />
        </v-card>
        <v-card class="ma-4">
          <v-simple-table dense v-if="chartData.length">
            <template v-slot:default>
              <thead>
                <tr>
                  <th
                    class="text-left"
                    v-for="(column, index) in columns"
                    :key="index"
                  >
                    {{ mapHeader(column) }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in chartData" :key="item.name">
                  <td v-for="(column, index) in columns" :key="index">
                    {{ displayFormt(item[column], column) }}
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
      <create-single-person-dialog
        ref="createSinglePersonDialog"
      ></create-single-person-dialog>
    </v-card>
  </v-dialog>
</template>

<script>
import XLSX from 'xlsx';
import moment from 'moment';
import axios from 'axios';

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
    promises: [],
    data: {
      name: '',
      description: '',
      address: '',
      city: '',
      zipCode: '',
    },
    columns: [
      'firstName',
      'lastName',
      'scoutName',
      'birthday',
      'street',
      'zipCodeShow',
      'phoneNumber',
      'email',
      'participantRole',
    ],
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
    displayFormt(date, column) {
      if (column === 'birthday') {
        return moment(date).format('DD.MM.YYYY');
      }
      if (column === 'participantRole') {
        return date === 1 ? 'Teilnehmer_innen' : 'Tagesgast';
      }
      return date;
    },
    mapHeader(column) {
      switch (column) {
        case 'firstName':
          return 'Vorname';
        case 'lastName':
          return 'Nachname';
        case 'scoutName':
          return 'Pfadfindername';
        case 'birthday':
          return 'Geburtstag';
        case 'street':
          return 'Straße';
        case 'zipCode':
          return 'PLZ';
        case 'phoneNumber':
          return 'Telefonnummer';
        case 'email':
          return 'E-Mail-Adresse';
        case 'participantRole':
          return 'Rolle';
        default:
          return 'Unbekannt';
      }
    },
    onFileChange(e) {
      const me = this;
      this.getJsonFromFile(e).then((data) => {
        me.processExcelData(data).then((data2) => {
          me.jsonData = data2;
        });
      });
    },
    async processExcelData(data) {
      const me = this;
      const output = [];
      let zipCodeTemps = [];
      data.forEach((element, index, array) => { // eslint-disable-line
        output.push(me.map(element));
      });
      await Promise.all(this.promises).then((array) => {
        zipCodeTemps = array;
      });
      output.forEach((element, index, array) => { // eslint-disable-line
        element.zipCode = zipCodeTemps[index][0].id; // eslint-disable-line
        element.zipCodeShow = `${zipCodeTemps[index][0].zipCode} - ${zipCodeTemps[index][0].city}`; // eslint-disable-line
      });
      return output;
    },
    getJsonFromFile(e) {
      return new Promise((resolve) => {
        const files = e.target.files; // eslint-disable-line
        const f = files[0]; // eslint-disable-line
        const reader = new FileReader(); // eslint-disable-line
        reader.onload = (e3) => {
          const data = new Uint8Array(e3.target.result); // eslint-disable-line
          const workbook = XLSX.read(data, { type: 'array' }); // eslint-disable-line
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
      const newInput = input;
      this.$refs.createSinglePersonDialog.openDialogEdit(newInput);
    },
    map(input) {
      const dto = {
        firstName: '',
        lastName: '',
        scoutName: '',
        street: '',
        zipCode: '',
        email: '',
        phoneNumber: '',
        birthday: new Date(),
        participantRole: '',
        eatHabitType: [],
        scoutGroup: 'Test',
      };
      dto.firstName = input['Vorname*'];
      dto.lastName = input['Nachname*'];
      dto.scoutName = input['Pfadfindername']; // eslint-disable-line
      dto.street = input['Adresse*'];
      dto.ageGroup = this.convertAgeGroup(input['Altersstufe*']);
      dto.zipCode = this.getZipCode(input['Postleitzahl*'], input['Stadt*']);
      dto.phoneNumber = input['Telefonnummer*'];
      dto.email = input['E-Mail-Adresse*'];
      dto.birthday = this.convertBirthday(input['Geburtsdatum*']);
      dto.participantRole = input['Tagesgast'] === 'x' ? 11 : 1; // eslint-disable-line
      return dto;
    },
    async callSingleZipCode(zipCode) {
      const path = `${this.API_URL}/basic/zip-code/?zip_city=${zipCode}`;
      const response = await axios.get(path);

      return response.data;
    },
    getZipCode(zipCode) {
      this.promises.push(this.callSingleZipCode(zipCode));
      return '...';
    },

    convertBirthday(birthdayDays) {
      const startDate = new Date(1900, 0, 1);
      const newDate = new Date(
        startDate.getFullYear(),
        startDate.getMonth(),
        startDate.getDate() + birthdayDays - 2,
      );
      return moment(newDate).format('YYYY-MM-DD');
    },
    convertAgeGroup(ageGroupString) {
      switch (ageGroupString) {
        case 'Meutenstufe':
          return 1;
        case 'Sippestufe':
          return 2;
        case 'Roverstufe':
          return 3;
        default:
          return null;
      }
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
