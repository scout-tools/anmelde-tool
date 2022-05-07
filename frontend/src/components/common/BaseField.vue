<template>
  <v-col :cols="field.cols ? field.cols : 6">
    <v-text-field
      v-if="field.fieldType === 'textfield'"
      :label="field.name"
      :value="value"
      @input="onInputChanged"
      :prepend-icon="field.icon"
      :error-messages="onErrorMessageChange(field.techName)"
      :disabled="field.disabled"
      :readonly="field.readonly"
      :filled="field.filled">
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-text-field>

    <v-text-field
      v-if="field.fieldType === 'number'"
      :label="field.name"
      :value="value"
      type="number"
      @input="onInputChanged"
      :prepend-icon="field.icon"
      :error-messages="onErrorMessageChange(field.techName)"
      :disabled="field.disabled"
      :readonly="field.readonly"
      :filled="field.filled"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-text-field>

    <v-textarea
      v-if="field.fieldType === 'textarea'"
      :label="field.name"
      :value="value"
      @input="onInputChanged"
      solo
      auto-grow
      :prepend-icon="field.icon"
      :error-messages="onErrorMessageChange(field.techName)"
      :disabled="field.disabled"
      :readonly="field.readonly"
      :filled="field.filled"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-textarea>

    <v-text-field
      v-if="field.fieldType === 'currency'"
      :label="field.name"
      :value="value"
      prefix="€"
      type="number"
      @input="onInputChanged"
      :prepend-icon="field.icon"
      :error-messages="onErrorMessageChange(field.techName)"
      :disabled="field.disabled"
      :readonly="field.readonly"
      :filled="field.filled"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-text-field>

    <v-autocomplete
      v-if="field.fieldType === 'refDropdown'"
      :label="field.name"
      :value="value"
      :items="lookupList"
      :prepend-icon="field.icon"
      required
      @input="onInputChanged"
      item-value="id"
      :item-text="getItemText"
      :error-messages="onErrorMessageChange(field.techName)"
    >
    </v-autocomplete>

    <v-combobox
      v-if="field.fieldType === 'refCombo'"
      :label="field.name"
      :value="value"
      :items="lookupList"
      :prepend-icon="field.icon"
      required
      chips
      multiple
      deletable-chips
      @input="onComboInputChanged"
      item-value="name"
      :item-text="getItemText"
      :error-messages="onErrorMessageChange(field.techName)"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-combobox>

    <v-combobox
      v-if="field.fieldType === 'simpleCombo'"
      :label="field.name"
      :value="value"
      :prepend-icon="field.icon"
      required
      chips
      multiple
      deletable-chips
      @input="onComboInputChanged"
      :error-messages="onErrorMessageChange(field.techName)"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-combobox>

    <v-select
      v-if="field.fieldType === 'refComboSingle'"
      :label="field.name"
      :value="value"
      :items="lookupList"
      :prepend-icon="field.icon"
      required
      @input="onInputChanged"
      item-value="id"
      :item-text="getItemText"
      :error-messages="onErrorMessageChange(field.techName)"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-select>

    <v-autocomplete
      v-if="field.fieldType === 'enumCombo'"
      :label="field.name"
      :value="enumValue"
      item-value="value"
      :items="convertEnum(this.lookupList)"
      :prepend-icon="field.icon"
      required
      @input="onInputChanged"
      :item-text="getItemText"
      :error-messages="onErrorMessageChange(field.techName)"
    >
      <template slot="append">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span>
            {{ field.tooltip }}
          </span>
        </v-tooltip>
      </template>
    </v-autocomplete>

    <v-autocomplete
      v-if="field.fieldType === 'zipField'"
      :label="field.name"
      :value="value"
      :items="lookupList"
      :prepend-icon="field.icon"
      required
      @input="onInputChanged"
      item-value="id"
      :loading="isLoading"
      :item-text="getItemText"
      :search-input.sync="search"
      :no-data-text="zipCodeNoDataText"
      :error-messages="onErrorMessageChange(field.techName)"
    >
    </v-autocomplete>
    <v-select
      v-if="field.fieldType === 'localRefDropdown'"
      :label="field.name"
      :value="value"
      :prepend-icon="field.icon"
      :items="field.referenceTable"
      required
      @input="onInputChanged"
      item-value="value"
      :item-text="field.referenceDisplay"
      :error-messages="onErrorMessageChange(field.techName)"
    >
    </v-select>
    <v-switch
      v-if="field.fieldType === 'checkbox'"
      :label="field.name"
      :input-value="value"
      @change="onInputChanged"
      :error-messages="onErrorMessageChange(field.techName)"
    >
    </v-switch>
    <v-container v-if="field.fieldType === 'radio'">
      <v-row class="mb-1">
        <v-icon class="mr-2"> {{ field.icon }}</v-icon>
        {{ field.name }}
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" class="mx-2" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span> {{ field.tooltip }}</span>
        </v-tooltip>
      </v-row>
      <v-row>
        <v-radio-group :value="value" @change="onRadioInputChanged">
          <v-radio
            v-for="choise in field.referenceTable"
            :key="choise.value"
            :label="choise.name"
            :value="choise.value"
          ></v-radio>
        </v-radio-group>
      </v-row>
    </v-container>
    <v-container v-if="field.fieldType === 'html'">
      <v-row class="mb-1">
        <v-icon class="mr-2"> {{ field.icon }}</v-icon>
        {{ field.name }}
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon color="info" class="mx-2" dark v-bind="attrs" v-on="on">
              mdi-help-circle-outline
            </v-icon>
          </template>
          <span> {{ field.tooltip }}</span>
        </v-tooltip>
      </v-row>
      <v-row>
        <ckeditor
          :editor="ckeditor.editor"
          :value="value"
          @input="onInputChanged"
          :config="ckeditor.editorConfig"
        ></ckeditor>
      </v-row>
    </v-container>
    <v-container v-if="field.fieldType === 'date'">
      <v-text-field
        :value="valueDate"
        v-mask="'##.##.####'"
        placeholder="DD.MM.YYYY"
        @input="onDateInputChanged"
        :label="`${field.name}`"
        :prepend-icon="field.icon"
        :error-messages="onErrorMessageChange(field.techName)"
        :disabled="field.disabled"
        :readonly="field.readonly"
        :filled="field.filled"
      >
        <template slot="append">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon color="info" dark v-bind="attrs" v-on="on">
                mdi-help-circle-outline
              </v-icon>
            </template>
            <span>
              {{ field.tooltip }}
            </span>
          </v-tooltip>
        </template>
      </v-text-field
      >
    </v-container>
    <v-container v-if="field.fieldType === 'datetime'">
      <v-row>
        <v-col>
          <v-text-field
            :value="valueDate"
            v-mask="'##.##.####'"
            placeholder="DD.MM.YYYY"
            @input="onDateTimeInputChangedDate"
            :label="`${field.name}-Datum (DD.MM.YYYY)`"
            :prepend-icon="field.icon"
            :error-messages="onErrorMessageChange(field.techName)"
            :disabled="field.disabled"
            :readonly="field.readonly"
            :filled="field.filled"
          >
            <template slot="append">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="info" dark v-bind="attrs" v-on="on">
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span>
                  {{ field.tooltip }}
                </span>
              </v-tooltip>
            </template>
          </v-text-field
          >
        </v-col>
        <v-col>
          <v-text-field
            :value="valueTime"
            v-mask="'##:##'"
            placeholder="HH:mm"
            @input="onDateTimeInputChangedTime"
            :label="`${field.name}-Uhrzeit (HH:mm)`"
            :prepend-icon="field.icon"
            :error-messages="onErrorMessageChange(field.techName)"
            :disabled="field.disabled"
            :readonly="field.readonly"
            :filled="field.filled"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
    <v-container v-if="field.fieldType === 'file'">
      <v-row>
        <v-col cols="6">
          <v-text-field :value="value" label="Datei"></v-text-field>
        </v-col>
        <v-col cols="1">
          <!-- 1. Create the button that will be clicked to select a file -->
          <v-btn small fab dark color="green" @click="handleFileImport">
            <v-icon> mdi-cloud-upload</v-icon>
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
            <v-icon> mdi-eye</v-icon>
          </v-btn>
        </v-col>
        <!-- Create a File Input that will be hidden but triggered with JavaScript -->
        <!-- <input
          ref="uploader"
          class="d-none"
          type="file"
          @change="onFileInputChanged"
        /> -->
      </v-row>
    </v-container>
  </v-col>
</template>

<script>
// import moment from 'moment'; // eslint-disable-line
// import { uuid } from 'vue-uuid';
import stepMixin from '@/mixins/stepMixin';
import serviceMixin from '@/mixins/serviceMixin';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import '@ckeditor/ckeditor5-build-classic/build/translations/de';

export default {
  props: {
    valdiationObj: {
      type: Object,
    },
    field: {
      type: Object,
      default: null,
      icon: null,
      tooltip: null,
      cols: 6,
    },
    value: {
      default: null,
    },
  },
  mixins: [stepMixin, serviceMixin],
  data() {
    return {
      itemsPerPage: 1000,
      lookupList: [],
      isSelecting: false,
      selectedFile: null,
      isLoading: false,
      search: null,
      zipCodeNoDataText: 'Bitte PLZ oder Ort eingeben.',
      ckeditor: {
        editor: ClassicEditor,
        editorData: '',
        editorConfig: {
          language: 'de',
        },
      },
    };
  },
  watch: {
    search(searchString) {
      // still loading
      if (this.loading) return;
      if (!searchString || searchString.indexOf(' ') >= 0 || searchString.length <= 1) {
        this.zipCodeNoDataText = 'Bitte PLZ oder Ort eingeben.';
        return;
      }
      this.loading = true;
      this.getZipCodeMapping(searchString)
        .then((res) => {
          this.lookupList = res;
          this.zipCodeNoDataText = 'Kein Treffer';
        })
        .catch((err) => {
          this.lookupList = null;
          this.zipCodeNoDataText = err.response.data.detail;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    enumValue() {
      this.onInputChanged(this.enumValue);
    },
  },
  computed: {
    valueDate() {
      return this.$moment(this.value)
        .format('DD.MM.YYYY', 'de');
    },
    valueTime() {
      return this.$moment(this.value)
        .format('HH:mm', 'de');
    },
    enumValue() {
      if (!this.lookupList) return '';
      const value = this.value; // eslint-disable-line
      const list = this.convertEnum(this.lookupList);
      if (list.filter((item) => item.value === value).length) {
        return value;
      }
      try {
        return list.filter((item) => item.name === value)[0].value;
      } catch (e) {
        return '';
      }
    },
  },
  methods: {
    convertEnum(list) {
      return list.map((x) => { // eslint-disable-line
        return {
          value: x[0],
          name: x[1],
        };
      });
    },
    onErrorMessageChange(field) {
      return this.errorMessage(field, this.valdiationObj);
    },
    async getData() {
      this.getLookup(this.field.lookupPath);
    },
    onInputChanged(value) {
      this.$emit('input', value);
    },
    onDateInputChanged(value) {
      const newDate = this.$moment(value, 'L', 'de');
      if (newDate.isValid() && value.length === 10) {
        this.onInputChanged(newDate.toDate());
      }
      this.$forceUpdate();
    },
    onDateTimeInputChangedDate(value) {
      const newDate = this.$moment(value, 'L', 'de');
      if (newDate.isValid() && value.length === 10) {
        this.onInputChanged(newDate.toDate());
      }
      this.$forceUpdate();
    },
    onComboInputChanged(value) {
      const returnArray = [];
      value.forEach((item) => {
        if (typeof item === 'object') {
          returnArray.push(item.name);
        } else {
          returnArray.push(item);
        }
      });
      this.$emit('input', returnArray);
      this.$forceUpdate();
    },
    onDateTimeInputChangedTime(value) {
      const newDate = this.$moment(
        `${this.valueDate} ${value}`,
        'DD.MM.YYYY hh:mm',
        'de',
      );
      if (newDate.isValid() && value.length === 5) {
        this.onInputChanged(newDate.toDate());
      }
      this.$forceUpdate();
    },
    onRadioInputChanged(value) {
      this.onInputChanged(value);
    },
    // async handleChange(file) {},
    // async onFileInputChanged(e) {},
    // handleFileImport() {
    //   this.isSelecting = true;

    //   // After obtaining the focus when closing the FilePicker, return the button state to normal
    //   window.addEventListener(
    //     'focus',
    //     () => {
    //       this.isSelecting = false;
    //     },
    //     { once: true },
    //   );

    //   // Trigger click on the FileInput
    //   this.$refs.uploader.click();
    // },
    // async showPdf() {},
    getItemText(item) {
      let template = '';
      this.field.lookupListDisplay.forEach((field, i) => {
        if (field.charAt(0) === '$') {
          template += field.substring(1, field.length);
        } else if (i === 0) {
          template += item[field];
        } else {
          template = `${template} - ${item[field]}`;
        }
      });
      return template;
    },
  },
  created() {
    if (
      this.field.fieldType === 'refDropdown' || // eslint-disable-line
      this.field.fieldType === 'enumCombo' || // eslint-disable-line
      this.field.fieldType === 'refComboSingle' || // eslint-disable-line
      this.field.fieldType === 'refCombo'
    ) {
      this.getData();
    }
    if (this.field.fieldType === 'zipField') {
      this.callSingleZipCode(this.value)
        .then((result) => {
          this.lookupList = result;
          this.$forceUpdate();
        });
    }
  },
};
</script>

<style scoped>
</style>
