<template>
  <v-form
    ref="forStartEndDeadline"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6">
      <span class="subtitle-1">
        Zeitraum der Aktion.
      </span>
      </v-row>
      <v-row class="ma-4">
        <v-dialog
          ref="dateRangeDialog"
          v-model="dialog.dateRange"
          :return-value.sync="data.dateRange"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="sortedDateRange"
              label="Wähle den Aktionszeitraum"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              required
              :error-messages="dateRangeErrors"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-if="dialog.dateRange"
            v-model="data.dateRange"
            no-title
            locale="de-DE"
            range
          />
          <v-spacer/>
          <v-btn
            color="primary"
            @click="dialog.dateRange = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="$refs.dateRangeDialog.save(data.dateRange)"
          >
            OK
          </v-btn>
        </v-dialog>
      </v-row>
      <v-row class="ma-4" v-if="data.dateRange.length > 0">
        <v-dialog
          ref="startTimeDialog"
          v-model="dialog.startTime"
          :return-value.sync="data.startTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.startTime"
              label="Wähle die Lagereröffnung"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              required
              :error-messages="startTimeErrors"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="dialog.startTime"
            v-model="data.startTime"
            format="24hr"
            range
            scrollable
          />
          <v-spacer/>
          <v-btn
            color="primary"
            @click="dialog.startTime = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="$refs.startTimeDialog.save(data.startTime)"
          >
            OK
          </v-btn>
        </v-dialog>
      </v-row>
      <v-row class="ma-4" v-if="data.dateRange.length > 0">
        <v-dialog
          ref="endTimeDialog"
          v-model="dialog.endTime"
          :return-value.sync="data.endTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.endTime"
              label="Wähle die Abschlussrunde"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              required
              :error-messages="endTimeErrors"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="dialog.endTime"
            v-model="data.endTime"
            format="24hr"
            range
            scrollable
          />
          <v-spacer/>
          <v-btn
            color="primary"
            @click="dialog.endTime = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="$refs.endTimeDialog.save(data.endTime)"
          >
            OK
          </v-btn>
        </v-dialog>
      </v-row>
      <v-row class="ma-4">
        <v-dialog
          ref="deadlineDateDialog"
          v-model="dialog.deadlineDate"
          :return-value.sync="data.deadlineDate"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.deadlineDate"
              label="Wähle die Deadline"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              required
              :error-messages="deadlineDateErrors"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-if="dialog.deadlineDate"
            v-model="data.deadlineDate"
            locale="de-DE"
          />
          <v-spacer/>
          <v-btn
            color="primary"
            @click="dialog.deadlineDate = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="$refs.deadlineDateDialog.save(data.deadlineDate)"
          >
            OK
          </v-btn>
        </v-dialog>
      </v-row>
      <v-row class="ma-4" v-if="data.deadlineDate.length > 0">
        <v-dialog
          ref="deadlineTimeDialog"
          v-model="dialog.deadlineTime"
          :return-value.sync="data.deadlineTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.deadlineTime"
              label="Wähle die Deadline Zeit"
              prepend-icon="mdi-clock-time-four-outline"
              readonly
              required
              :error-messages="deadlineTimeErrors"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="dialog.deadlineTime"
            v-model="data.deadlineTime"
            format="24hr"
            range
            scrollable
          />
          <v-spacer/>
          <v-btn
            color="primary"
            @click="dialog.deadlineTime = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="$refs.deadlineTimeDialog.save(data.deadlineTime)"
          >
            OK
          </v-btn>
        </v-dialog>
      </v-row>

      <v-divider class="my-2" v-if="false"/>
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepStartEndDeadline',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      dateRange: [],
      startTime: '',
      endTime: '',
      deadlineDate: '',
      deadlineTime: '',
    },
    dialog: {
      dateRange: false,
      startTime: false,
      endTime: false,
      deadlineDate: false,
      deadlineTime: false,
    },
  }),
  validations: {
    sortedDateRange: {
      required,
    },
    data: {
      startTime: {
        required,
      },
      endTime: {
        required,
      },
      deadlineDate: {
        required,
      },
      deadlineTime: {
        required,
      },
    },
  },
  computed: {
    sortedDateRange() {
      const dateRangeCopy = Array.from(this.data.dateRange);
      return dateRangeCopy.sort((date1, date2) => new Date(date1) - new Date(date2));
    },
    sortedAndParsedDateRange() {
      return this.sortedDateRange.map((date) => new Date(date));
    },
    startDate() {
      if (this.sortedAndParsedDateRange.length < 1) {
        return '';
      }
      return this.sortedAndParsedDateRange[0].toLocaleDateString();
    },
    endDate() {
      switch (this.sortedAndParsedDateRange.length) {
        case 1:
          return this.sortedAndParsedDateRange[0].toLocaleDateString();
        case 2:
          return this.sortedAndParsedDateRange[1].toLocaleDateString();
        default:
          return '';
      }
    },
    dateRangeErrors() {
      const errors = [];
      if (!this.$v.sortedDateRange.$dirty) return errors;
      if (!this.$v.sortedDateRange.required) {
        errors.push('Ein Datum muss eingetragen werden.');
      }
      return errors;
    },
    startTimeErrors() {
      const errors = [];
      if (!this.$v.data.startTime.$dirty) return errors;
      if (!this.$v.data.startTime.required) {
        errors.push('Eine Startzeit muss eingetragen werden.');
      }
      return errors;
    },
    endTimeErrors() {
      const errors = [];
      if (!this.$v.data.endTime.$dirty) return errors;
      if (!this.$v.data.endTime.required) {
        errors.push('Eine Endzeit muss eingetragen werden.');
      }
      return errors;
    },
    deadlineDateErrors() {
      const errors = [];
      if (!this.$v.data.deadlineDate.$dirty) return errors;
      if (!this.$v.data.deadlineDate.required) {
        errors.push('Eine Deadline muss eingetragen werden.');
      }
      return errors;
    },
    deadlineTimeErrors() {
      const errors = [];
      if (!this.$v.data.deadlineTime.$dirty) return errors;
      if (!this.$v.data.deadlineTime.required) {
        errors.push('Eine Deadline Zeit muss eingetragen werden.');
      }
      return errors;
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        // startTime: this.data.startTime,
        // endTime: this.data.endTime,
        // deadline: this.data.deadlineDate,
      };
    },
  },
};
</script>
