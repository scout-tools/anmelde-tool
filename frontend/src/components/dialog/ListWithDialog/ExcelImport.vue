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
        <template>
          Lade hier deine Excel Datei hoch, um dir die manuelle Eingabe zu
          erleichtern. Die Datei muss in einem bestimmten Format sein.
          <a style="color: blue" target="_blank" :href="cloudLink">
            Link zur Cloud
          </a>
        </template>
        <v-card class="ma-4 pa-3">
          <label for="firstName">
            <input type="file" @change="onFileChange" id="firstName" />
          </label>
        </v-card>
        <v-card class="ma-4">
          <v-simple-table dense v-if="chartData.length">
            <template v-slot:default>
              <thead>
                <tr>
                  <th
                    class="text-left"
                    v-for="(column, index) in dialogMeta.fields"
                    :key="index"
                  >
                    {{ column.name }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in chartData" :key="row.name">
                  <td v-for="(column, index) in dialogMeta.fields" :key="index">
                    {{
                      displayFormt(
                        row[column['techName']],
                        column['techName'],
                        row,
                      )
                    }}
                  </td>
                  <td>
                    <v-btn icon @click="fillParticipant(row)">
                      <v-icon> mdi-cloud-upload </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-sheet>
      <CreateModalExcel
        ref="createModalExel"
        :dialogMeta="dialogMeta"
        @refresh="onRefresh()"
        :valdiationObj="valdiationObj"
        @validate="validate"
      />
      <upload-excel-file ref="uploadExcelFile" @refresh="onRefresh()" />
    </v-card>
  </v-dialog>
</template>

<script>
import { read, utils } from 'xlsx';
import moment from 'moment';
import axios from 'axios';

import CreateModal from './CreateModal.vue';

export default {
  components: {
    CreateModalExcel: CreateModal,
  },
  props: {
    dialogMeta: {
      default: {},
    },
    valdiationObj: {},
    currentEvent: {
      default: {},
    },
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
    validate(data) {
      this.$emit('validate', data);
    },
    displayFormt(value, column, row) {
      if (column === 'zipCode') {
        return row.zipCodeShow;
      }
      if (column === 'birthday') {
        return moment(row.birthday).format('DD.MM.YYYY');
      }
      if (column === 'eatHabit') {
        return row.eatHabit.join(', ');
      }
      if (column === 'gender') {
        const fieldDef = this.dialogMeta.fields.filter(
          (field) => field.techName === 'gender',
        )[0];
        return fieldDef.referenceTable.filter(
          (item) => item.value === row.gender,
        )[0].name;
      }
      return value;
    },
    onFileChange(e) {
      const me = this;
      this.getJsonFromFile(e).then((data) => {
        const cleanData = this.keeoValid(data);
        me.processExcelData(cleanData).then((data2) => {
          me.jsonData = data2;
        });
      });
    },
    async processExcelData(data) {
      const me = this;
      const output = [];
      let zipCodeTemps = [];
      data.forEach((element) => {
        output.push(me.map(element)); // eslint-disable-line
      });
      await Promise.all(this.promises).then((array) => {
        zipCodeTemps = array;
      });
      output.forEach((element, index) => {
        element.zipCode = zipCodeTemps[index][0].id; // eslint-disable-line
        element.zipCodeShow = `${zipCodeTemps[index][0].zipCode} - ${zipCodeTemps[index][0].city}`; // eslint-disable-line
      });
      return output;
    },
    getJsonFromFile(e) {
      console.log(read);
      return new Promise((resolve) => {
        const files = e.target.files; // eslint-disable-line
        const f = files[0]; // eslint-disable-line
        e.target.value = '';
        const reader = new FileReader(); // eslint-disable-line
        reader.onload = (e3) => {
          console.log(read);
          const data = new Uint8Array(e3.target.result); // eslint-disable-line
          const workbook = read(data, { type: 'array' }); // eslint-disable-line
          const firstWorksheet = workbook.Sheets[workbook.SheetNames[0]];
          const dataExport = utils.sheet_to_json(firstWorksheet, {
            blankRows: false,
            header: 2,
            defval: '',
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
      this.$refs.createModalExel.openDialog(newInput);
    },
    map(input) {
      const dto = input;

      if (dto.leaderType) {
        dto.leader = dto.leaderType;
      }
      if (dto.gender) {
        dto.gender = dto.gender.toUpperCase();
      }

      if (dto.participantRole) {
        dto.bookingOption = dto.participantRole;
      }

      if (dto.eatHabitType) {
        dto.eatHabit = [dto.eatHabitType];
      }

      dto.zipCode = this.getZipCode(input.zipCode, input.city); // eslint-disable-line
      dto.birthday = this.convertBirthday(input.birthday);
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
      return newDate;
    },
    removeEmpty(obj) {
      return Object.entries(obj)
        .filter(([_, v]) => v !== '') // eslint-disable-line
        .reduce((acc, [k, v]) => ({ ...acc, [k]: v }), {});
    },
    keeoValid(inputData) {
      const primariyObj = inputData[2];
      const data = inputData;
      const cleanContent = [];
      if (primariyObj) {
        const primaries = this.removeEmpty(primariyObj);
        const primaryArray = Object.keys(primaries);
        const content = data.splice(3);

        content.forEach((item) => {
          const hasValidPrimaryKey = (currentValue) =>
            item[currentValue] !== ''; // eslint-disable-line
          if (primaryArray.every(hasValidPrimaryKey)) {
            cleanContent.push(item);
          }
        });
      }

      return cleanContent;
    },
  },
  computed: {
    cloudLink() {
      debugger;
      return this.currentEvent.cloudLink;
    },
    chartData() {
      return this.jsonData;
    },
  },
};
</script>

<style>
</style>
