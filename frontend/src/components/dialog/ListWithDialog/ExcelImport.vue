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
          <v-container>
            <v-row align="center" justify="center">
              <v-col cols="6" align="center" justify="center">
                <v-file-input
                  label="Wähle eine passende Exceldatei aus."
                  show-size
                  truncate-length="20"
                  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  @change="onFileChange"
                ></v-file-input>
              </v-col>
              <v-col cols="4" align="center" justify="center">
                <v-radio-group
                  v-model="filterSelection"
                  row
                  v-show="jsonData && jsonData.length">
                  <v-radio label="Nur nicht Angemeldete" value="new"></v-radio>
                  <v-radio label="Nur bereits Angemeldete" value="old"></v-radio>
                </v-radio-group>
              </v-col>
              <v-col cols="2" v-show="jsonData && jsonData.length">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="info" class="mx-2" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    Wähle aus welche Daten aus der Excel Tabelle
                     angezeigt werden sollen. Diese darstellug
                      soll dir helfen keine Doppelten Einträge hinzuzufügen.
                  </span>
                </v-tooltip>
              </v-col>
            </v-row>
          </v-container>
        </v-card>
        <v-card class="ma-4" v-show="!isLoading">
          <v-simple-table dense v-if="chartData.length">
            <template v-slot:default>
              <thead>
                <tr>
                  <th>Upload</th>
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
                  <td>
                    <v-tooltip bottom>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          v-bind="attrs"
                          v-on="on"
                          color="success"
                          icon
                          @click="fillParticipant(row)"
                        >
                          <v-icon> mdi-cloud-upload </v-icon>
                        </v-btn>
                      </template>
                      <span>Diese Person anmelden</span>
                    </v-tooltip>
                  </td>
                  <td v-for="(column, index) in dialogMeta.fields" :key="index">
                    {{
                      displayFormt(
                        row[column['techName']],
                        column['techName'],
                        row,
                      )
                    }}
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
        <v-container v-show="isLoading">
          <Circual />
        </v-container>
      </v-sheet>
      <CreateModalExcel
        ref="createModalExel"
        :dialogMeta="dialogMeta"
        @refresh="onRefresh()"
        :valdiationObj="valdiationObj"
        @validate="validate"
      />
    </v-card>
  </v-dialog>
</template>

<script>
import { read, utils } from 'xlsx';
import moment from 'moment';
import axios from 'axios';
import serviceMixin from '@/mixins/serviceMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';

import Circual from '@/components/loading/Circual.vue';
import CreateModal from './CreateModal.vue';

export default {
  components: {
    CreateModalExcel: CreateModal,
    Circual,
  },
  mixins: [serviceMixin, apiCallsMixin],
  props: {
    dialogMeta: {
      default: {},
    },
    valdiationObj: {},
    currentEvent: {
      type: Object,
      default: () => ({}),
    },
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    files: [],
    filterSelection: 'new',
    promises: [],
    isLoading: false,
    primaryArray: [],
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
    eatHabitList: [],
    leaderList: [],
    bookingOptionList: [],
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
      if (column === 'eatHabit' && row.eatHabit && row.eatHabit.length > 0) {
        return row.eatHabit.join(', ');
      }
      if (column === 'gender') {
        try {
          const fieldDef = this.dialogMeta.fields.filter(
            (field) => field.techName === 'gender',
          )[0];
          return fieldDef.referenceTable.filter(
            (item) => item.value === row.gender,
          )[0].name;
        } catch (e) {
          console.log('Fehler');
        }
      }
      if (column === 'leader') {
        try {
          return this.leaderList.filter(
            (field) => field.value === row.leader,
          )[0].name;
        } catch (e) {
          console.log('Fehler');
        }
      }
      if (column === 'bookingOption') {
        try {
          return this.bookingOptionList.filter(
            (field) => field.id === row.bookingOption,
          )[0].name;
        } catch (e) {
          console.log('Fehler');
        }
      }
      return value;
    },
    onFileChange(e) {
      this.isLoading = true;
      const me = this;
      console.log(e);
      this.getJsonFromFile(e).then((data) => {
        console.log(e);
        const cleanData = this.keepValid(data);
        const trimmedArray = [];
        me.processExcelData(cleanData).then((data2) => {
          data2.forEach((row) => {
            trimmedArray.push(this.trimObjValues(row));
          });
          me.jsonData = trimmedArray;
          this.isLoading = false;
        });
      });
    },
    trimObjValues(obj) {
      return Object.keys(obj).reduce((acc, curr) => {
        acc[curr] = typeof obj[curr] === 'string' ? obj[curr].trim() : obj[curr];
        return acc;
      }, {});
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
        if (zipCodeTemps[index] && zipCodeTemps[index].length) {
          element.zipCode = zipCodeTemps[index][0].id; // eslint-disable-line
          element.zipCodeShow = `${zipCodeTemps[index][0].zipCode} - ${zipCodeTemps[index][0].city}`; // eslint-disable-line
        }
      });
      return output;
    },
    getJsonFromFile(e) {
      return new Promise((resolve) => {
        const reader = new FileReader(); // eslint-disable-line
        reader.onload = (e3) => {
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
        if (e) {
          reader.readAsArrayBuffer(e);
        } else {
          this.jsonData = [];
          this.isLoading = false;
        }
      });
    },
    onClickOk() {
      this.active = false;
    },
    openDialog() {
      this.active = true;
      this.refresh();
    },
    closeDialog() {
      this.active = false;
      this.$emit('refresh');
    },
    fillParticipant(input) {
      const newInput = input;
      this.$refs.createModalExel.openDialog(newInput);
    },
    convertLeader(inPutString) {
      const mapping = {
        normal: 'N',
        'Kein Amt': 'N',
        Stammesführung: 'StaFue',
        Sippenführung: 'SiFue',
        Meutenführung: 'MeuFue',
        Roverrundenführung: 'RoFue',
      };
      return mapping[inPutString] || mapping.normal;
    },
    convertEatHabit(inPutString) {
      const mapping = {
        normal: null, // eslint-disable-line
        Vegetarisch: 'Kein Fleisch (Vegetarisch)', // eslint-disable-line
        Vegan: 'Keine Tierprodukte (Vegan)', // eslint-disable-line
        'kein Gluten': 'Kein Gluten', // eslint-disable-line
        'Keine Hüsenfrüchte': 'Keine Hülsenfrüchte', // eslint-disable-line
        'Keine Laktose': 'Kein Laktose', // eslint-disable-line
        'Keine Eier': 'Keine Eier', // eslint-disable-line
      };
      return mapping[inPutString] || mapping.normal;
    },
    convertBookingOption(inPutString) {
      const mapping = {
        normal: null,
        Kaperfahrt: 3,
        Bundeslager: 4,
        'Bundeslager + Kaperfahrt': 5,
        'Tagesgast Mittwoch': 6,
        'Tagesgast Donnerstag': 7,
        'Tagesgast Freitag': 8,
      };
      return mapping[inPutString] || mapping.normal;
    },
    convertGender(inPutString) {
      const mapping = {
        normal: null, // eslint-disable-line
        m: 'M', // eslint-disable-line
        w: 'F', // eslint-disable-line
        d: 'D', // eslint-disable-line
        '-': 'N', // eslint-disable-line
      };
      return mapping[inPutString.toLowerCase()] || mapping.normal;
    },
    map(input) {
      const dto = input;

      if (dto.leaderType) {
        dto.leader = this.convertLeader(dto.leaderType);
      }
      if (dto.gender) {
        dto.gender = this.convertGender(dto.gender);
      }

      if (dto.participantRole) {
        dto.bookingOption = this.convertBookingOption(dto.participantRole);
      }

      if (dto.eatHabitType) {
        const eatHabitType = this.convertEatHabit(dto.eatHabitType);
        dto.eatHabit = [];
        if (eatHabitType) {
          dto.eatHabit.push(eatHabitType);
        }
        if (dto.eatHabitText) {
          dto.eatHabit.push(dto.eatHabitText);
        }
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
      return null;
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
    keepValid(inputData) {
      const primariyObj = inputData[2];
      const data = inputData;
      const cleanContent = [];
      if (primariyObj) {
        const primaries = this.removeEmpty(primariyObj);
        const primaryArray = Object.keys(primaries);
        this.primaryArray = primaryArray;
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
    convertEnum(list) {
      return list.map((x) => { // eslint-disable-line
        return {
          value: x[0],
          name: x[1],
        };
      });
    },
    onRefresh() {
      this.refresh();
    },
    refresh() {
      this.isLoading = true;
      axios
        .all([
          this.getSimpleService('/basic/eat-habits/'),
          this.getSimpleService('/event/leader-types/'),
          this.getSimpleService(
            `/event/event/${this.currentEvent.id}/booking-options/`, // eslint-disable-line
          ),
          this.getService(this.dialogMeta.path),
        ])
        .then(
          axios.spread(
            (firstResponse, secondResponse, thirdResponse, fifthResponse) => {
              this.eatHabitList = firstResponse.data;
              this.leaderList = this.convertEnum(secondResponse.data);
              this.bookingOptionList = thirdResponse.data;
              this.items = fifthResponse.data;
              this.isLoading = false;
              this.$forceUpdate();
            },
          ),
        )
        .catch((error) => {
          console.error(error);
          this.isLoading = false;
        });
    },
  },
  computed: {
    cloudLink() {
      return this.currentEvent.cloudLink;
    },
    chartData() {
      const returnData = [];
      this.jsonData.forEach((row) => {
        const matchFirstname = !!this.items.filter(
          (item) => item.firstName.trim() === row.firstName.trim(),
        ).length;
        const matchLastname = !!this.items.filter(
          (item) => item.lastName.trim() === row.lastName.trim(),
        ).length;
        if (this.filterSelection === 'new') {
          if ((!matchFirstname || !matchLastname) && row.firstName.length > 0) {
            returnData.push(row);
          }
        } else {
          if (matchFirstname && matchLastname) { // eslint-disable-line
            returnData.push(row);
          }
        }
      });
      return returnData;
    },
  },
};
</script>

<style>
</style>
