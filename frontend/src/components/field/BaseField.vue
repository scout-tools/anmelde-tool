<template>
  <v-row>
    <v-text-field
      v-if="field.fieldType === 'textfield'"
      :label="field.name"
      :value="value"
      @input="onInputChanged"
    >
    </v-text-field>
    <v-autocomplete
      v-if="field.fieldType === 'refDropdown'"
      :label="field.name"
      :value="value"
      :items="getRefList"
      required
      @input="onInputChanged"
      item-value="id"
      :item-text="getItemText"
    >
    </v-autocomplete>
    <v-select
      v-if="field.fieldType === 'localRefDropdown'"
      :label="field.name"
      :value="value"
      :items="field.referenceTable"
      required
      @input="onInputChanged"
      item-value="id"
      :item-text="field.referenceDisplay"
    >
    </v-select>
    <v-switch
      v-if="field.fieldType === 'checkbox'"
      :label="field.name"
      :input-value="value"
      @change="onInputChanged"
    >
    </v-switch>
    <v-col v-if="field.fieldType === 'date'">
      <v-text-field
        :value="value"
        v-mask="'##/##/####'"
        placeholder="DD/MM/YYYY"
        @input="onDateInputChanged"
        :label="`${field.name}`"
      ></v-text-field>
    </v-col>
    <v-container v-if="field.fieldType === 'file'">
      <v-row>
        <v-col cols="6">
          <v-text-field
            :value="value"
            v-model="value"
            label="Datei"
          ></v-text-field>
        </v-col>
        <v-col cols="1">
          <!-- 1. Create the button that will be clicked to select a file -->
          <v-btn small fab dark color="green" @click="handleFileImport">
            <v-icon> mdi-cloud-upload </v-icon>
          </v-btn>
        </v-col>
        <v-col cols="1">
          <v-btn
            small
            fab
            dark
            color="darkgrey"
            :disabled="!value"
            @click="showPdf"
          >
            <v-icon> mdi-eye </v-icon>
          </v-btn>
        </v-col>
        <!-- Create a File Input that will be hidden but triggered with JavaScript -->
        <input
          ref="uploader"
          class="d-none"
          type="file"
          @change="onFileInputChanged"
        />
      </v-row>
    </v-container>
  </v-row>
</template>

<script>
import moment from "moment"; // eslint-disable-line
import { uuid } from "vue-uuid";

export default {
  props: {
    field: {
      type: Object,
      default: null,
    },
    value: {
      default: null,
    },
  },
  data() {
    return {
      itemsPerPage: 1000,
      getRefList: [],
      isSelecting: false,
      selectedFile: null,
    };
  },
  methods: {
    async getData(componentName) {
      let queryName = [];
    },
    async getQuery(queryName) {},
    onInputChanged(value) {
      console.log(value);
      this.$emit("input", value);
    },
    onDateInputChanged(value) {
      const newDate = this.$moment(value, "L", "de");
      if (newDate.isValid()) {
        this.onInputChanged(value);
      }
      this.$forceUpdate();
    },
    async handleChange(file) {},
    async onFileInputChanged(e) {},
    handleFileImport() {
      this.isSelecting = true;

      // After obtaining the focus when closing the FilePicker, return the button state to normal
      window.addEventListener(
        "focus",
        () => {
          this.isSelecting = false;
        },
        { once: true }
      );

      // Trigger click on the FileInput
      this.$refs.uploader.click();
    },
    async showPdf() {},
    getItemText(item) {
      let template = "";
      this.field.referenceListDisplay.forEach((field, i) => {
        if (i === 0) {
          template = template + item[field];
        } else {
          template = template + " - " + item[field];
        }
      });
      return template;
    },
  },
  created() {
    if (this.field.fieldType === "refDropdown") {
      this.getData(this.field.referenceTable);
    }
  },
};
</script>

<style scoped>
</style>