<template>
  <v-form
    ref="forStartEndDeadline"
    v-model="valid"
  >
    <v-container>
      <v-row class="my-6">
      <span class="subtitle-1">
        Zeitraum der Aktion.
      </span>
      </v-row>
      <v-row>
        <v-dialog
          ref="dateRangeDialog"
          v-model="dialog.dateRange"
          :return-value.sync="data.dateRange"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="sortedDateRangeString"
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
            v-model="data.dateRange"
            no-title
            range
          />
          <v-spacer/>
          <picker-dialog-buttons @cancel="dialog.dateRange = false"
                                 @ok="$refs.dateRangeDialog.save(data.dateRange)"/>
        </v-dialog>
      </v-row>
      <v-row>
        <v-dialog
          ref="startTimeDialog"
          v-model="dialog.startTime"
          :return-value.sync="data.startTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.startTime"
              :disabled="!dataRangeIsFilled"
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
            :disabled="!dialog.startTime"
            v-model="data.startTime"
            format="24hr"
            range
            scrollable
          />
          <v-spacer/>
          <picker-dialog-buttons @cancel="dialog.startTime = false"
                          @ok="$refs.startTimeDialog.save(data.startTime)"/>
        </v-dialog>
      </v-row>
      <v-row>
        <v-dialog
          ref="endTimeDialog"
          v-model="dialog.endTime"
          :return-value.sync="data.endTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.endTime"
              :disabled="!dataRangeIsFilled"
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
          <picker-dialog-buttons @cancel="dialog.endTime = false"
                          @ok="$refs.endTimeDialog.save(data.endTime)"/>
        </v-dialog>
      </v-row>
      <v-row>
        <v-dialog
          ref="deadlineDateDialog"
          v-model="dialog.deadlineDate"
          :return-value.sync="data.deadlineDate"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="deadlineDateString"
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
          />
          <v-spacer/>
          <picker-dialog-buttons @cancel="dialog.deadlineDate = false"
                          @ok="$refs.deadlineDateDialog.save(data.deadlineDate)"/>
        </v-dialog>
      </v-row>
      <v-row>
        <v-dialog
          ref="deadlineTimeDialog"
          v-model="dialog.deadlineTime"
          :return-value.sync="data.deadlineTime"
          width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="data.deadlineTime"
              :disabled="!deadlineIsFilled"
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
          <picker-dialog-buttons @cancel="dialog.deadlineTime = false"
                          @ok="$refs.deadlineTimeDialog.save(data.deadlineTime)"/>
        </v-dialog>
      </v-row>

      <v-divider class="my-2"/>
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import moment from 'moment';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import PickerDialogButtons from '../components/button/PickerDialogButtons.vue';

export default {
  name: 'StepStartEndDeadline',
  props: ['position', 'maxPos'],
  components: {
    PickerDialogButtons,
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      dateRange: [],
      startTime: '18:00',
      endTime: '13:00',
      deadlineDate: '',
      deadlineTime: '00:00',
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
      const rangeArray = Array.from(this.data.dateRange);
      if (rangeArray[0] === rangeArray[1]) {
        rangeArray.pop();
        return rangeArray;
      }
      return rangeArray.sort((date1, date2) => new Date(date1) - new Date(date2));
    },
    sortedDateRangeString() {
      const dateFormat = 'DD.MM.YYYY';
      const range = this.sortedDateRange;
      switch (range.length) {
        case 1:
          return `${moment(range[0]).format(dateFormat)}`;
        case 2:
          return `${moment(range[0]).format(dateFormat)} - ${moment(range[1]).format(dateFormat)}`;
        default:
          return '';
      }
    },
    dataRangeIsFilled() {
      return this.sortedDateRange.length > 0;
    },
    deadlineIsFilled() {
      return this.data.deadlineDate !== '';
    },
    deadlineDateString() {
      const dateFormat = 'DD.MM.YYYY';
      if (this.data.deadlineDate === '') {
        return '';
      }
      return `${moment(this.data.deadlineDate).format(dateFormat)}`;
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
        startTime: moment(`${this.sortedDateRange[0]} ${this.data.startTime}`),
        endTime: moment(`${this.sortedDateRange[1]} ${this.data.endTime}`),
        registrationDeadline: moment(`${this.data.deadlineDate} ${this.data.deadlineTime}`),
      };
    },
  },
};
</script>
