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
    <v-container v-if="field.fieldType === 'radio'">
      <v-row class="mb-1">
        <v-icon class="mr-2"> {{ field.icon }} </v-icon>
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
        <v-icon class="mr-2"> {{ field.icon }} </v-icon>
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
        :value="value"
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
        </template></v-text-field
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
            </template></v-text-field
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
      ckeditor: {
        editor: ClassicEditor,
        editorData: '',
        editorConfig: {
          language: 'de',
        },
      },
    };
  },
  computed: {
    valueDate() {
      return this.$moment(this.value).format('DD.MM.YYYY', 'de');
    },
    valueTime() {
      return this.$moment(this.value).format('HH:mm', 'de');
    },
  },
  methods: {
    onErrorMessageChange(field) {
      return this.errorMessage(field, this.valdiationObj);
    },
    async getData() {
      this.getLookup(this.field.lookupPath);
    },
    onInputChanged(value) {
      this.$emit('input', value);
    },
    onDateTimeInputChangedDate(value) {
      const newDate = this.$moment(value, 'L', 'de');
      if (newDate.isValid() && value.length === 10) {
        this.onInputChanged(newDate.toDate());
      }
      this.$forceUpdate();
    },
    onDateTimeInputChangedTime(value) {
      if (value.length !== 5) {
        return;
      }
      const newDate = this.$moment(
        `${this.valueDate} ${value}`,
        'DD.MM.YYYY hh:mm',
        'de',
      );
      if (newDate.isValid()) {
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
        if (i === 0) {
          template += item[field];
        } else {
          template = `${template}  - ${item[field]}`;
        }
      });
      return template;
    },
  },
  created() {
    if (this.field.fieldType === 'refDropdown') {
      this.getData(this.field.referenceTable);
    }
  },
};
</script>

<style scoped>
</style>
