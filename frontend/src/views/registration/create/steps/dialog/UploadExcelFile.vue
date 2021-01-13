<template>
  <v-dialog
    ref="deadlineDateDialog"
    v-model="active"
    transition="dialog-top-transition"
    fullscreen
  >
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Excel Datei importieren</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-sheet class="ma-5">
        <v-header>
          Lade deine Excel Datei hoch um dir die Manuelle eingabe zu erleichern
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
                    <v-btn icon>
                      <v-icon> mdi-cloud-upload </v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-card>
      </v-sheet>
    </v-card>
  </v-dialog>
</template>

<script>
import XLSX from 'xlsx';

export default {
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
        debugger;
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
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.active = true;
    },
    closeDialog() {
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
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
