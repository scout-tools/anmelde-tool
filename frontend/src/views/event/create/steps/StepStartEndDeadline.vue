<template>
  <v-form ref="forStartEndDeadline" v-model="valid">
    <v-container>
      <v-row class="my-6">
        <span class="subtitle-1"> Zeitraum der Aktion. </span>
      </v-row>
      <v-row>
        <DateTimePicker
          ref="startTimeRef"
          v-model="data.startTime"
          :errorMessagesTime="startTimeErrors"
          :errorMessagesDate="startTimeErrors"
          title="Aktionstart"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="endTimeRef"
          v-model="data.endTime"
          title="Aktionende"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="registrationStartRef"
          v-model="data.registrationStart"
          title="Anmeldestart"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="registrationDeadlineRef"
          v-model="data.registrationDeadline"
          title="Anmeldeende"
        />
      </v-row>

      <v-divider class="my-2" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep()"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import moment from 'moment';
import { required } from 'vuelidate/lib/validators';
import { stepMixin } from '@/mixins/stepMixin';

import DateTimePicker from '@/components/picker/DateTimePicker.vue';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepStartEndDeadline',
  props: ['position', 'maxPos', 'data'],
  components: {
    PrevNextButtons,
    DateTimePicker,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      valid: true,
    };
  },
  mixins: [stepMixin],
  validations: {
    data: {
      startTime: {
        required,
      },
      endTime: {
        required,
      },
      registrationStart: {
        required,
      },
      registrationDeadline: {
        required,
      },
    },
  },
  computed: {
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
      if (this.$v.data.deadlineDate.$invalid) {
        errors.push('Gib ein Datum vor dem Starttermin ein.');
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
    getData() {
      return {
        startTime: this.data.startTime,
        endTime: this.data.endTime,
        registrationStart: this.data.registrationStart,
        registrationDeadline: this.data.registrationDeadline,
      };
    },
  },
  mounted() {
    this.$refs.startTimeRef.setDate(this.data.startTime);
    this.$refs.endTimeRef.setDate(this.data.endTime);
    this.$refs.registrationStartRef.setDate(this.data.registrationStart);
    this.$refs.registrationDeadlineRef.setDate(this.data.registrationDeadline);
  },
};
</script>
