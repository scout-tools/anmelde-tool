<template>
  <v-form ref="forStartEndDeadline" v-model="valid">
    <v-container>
      <v-row class="my-6">
        <span class="subtitle-1"> Zeitraum der Aktion. </span>
      </v-row>
      <v-row>
        <DateTimePicker
          ref="startTimeRef"
          v-model="startTime"
          :errorMessagesTime="startTimeErrors"
          :errorMessagesDate="startTimeErrors"
          title="Aktionstart"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="endTimeRef"
          v-model="endTime"
          title="Aktionende"
          :errorMessagesTime="endTimeErrors"
          :errorMessagesDate="endTimeErrors"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="registrationStartRef"
          v-model="registrationStart"
          title="Anmeldestart"
          :error-messages-date="registrationStartTimeErrors"
          :error-messages-time="registrationStartTimeErrors"
        />
      </v-row>
      <v-row>
        <DateTimePicker
          ref="registrationDeadlineRef"
          v-model="registrationDeadline"
          title="Anmeldeende"
          :error-messages-date="registrationEndTimeErrors"
          :error-messages-time="registrationEndTimeErrors"
        />
      </v-row>
      <v-divider class="my-2"/>
      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
        @ignore="onIngoredClicked"
      />
    </v-container>
  </v-form>
</template>

<script>
import moment from 'moment';
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import DateTimePicker from '@/components/picker/DateTimePicker.vue';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';

export default {
  name: 'StepStartEndDeadline',
  header: 'Daten und Uhrzeit',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
    DateTimePicker,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      valid: true,
      startTime: null,
      endTime: null,
      registrationDeadline: null,
      registrationStart: null,
      deadlineDate: null,
    };
  },
  mixins: [stepMixin],
  validations: {
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
  computed: {
    deadlineIsFilled() {
      return this.deadlineDate !== '';
    },
    deadlineDateString() {
      const dateFormat = 'DD.MM.YYYY';
      if (this.deadlineDate === '') {
        return '';
      }
      return `${moment(this.data.deadlineDate, dateFormat, 'de')
        .format(dateFormat)}`;
    },
    startTimeErrors() {
      const errors = [];
      if (!this.$v.startTime.$dirty) return errors;
      if (!this.$v.startTime.required) {
        errors.push('Eine Startzeit muss eingetragen werden.');
      }
      return errors;
    },
    endTimeErrors() {
      const errors = [];
      if (!this.$v.endTime.$dirty) return errors;
      if (!this.$v.endTime.required) {
        errors.push('Eine Endzeit muss eingetragen werden.');
      }
      return errors;
    },
    deadlineDateErrors() {
      const errors = [];
      if (!this.$v.deadlineDate.$dirty) return errors;
      if (!this.$v.deadlineDate.required) {
        errors.push('Eine Deadline muss eingetragen werden.');
      }
      if (this.$v.deadlineDate.$invalid) {
        errors.push('Gib ein Datum vor dem Starttermin ein.');
      }
      return errors;
    },
    deadlineTimeErrors() {
      const errors = [];
      if (!this.$v.deadlineTime.$dirty) return errors;
      if (!this.$v.deadlineTime.required) {
        errors.push('Eine Deadline Zeit muss eingetragen werden.');
      }
      return errors;
    },
    registrationStartTimeErrors() {
      const errors = [];
      if (!this.$v.registrationStart.$dirty) return errors;
      if (!this.$v.registrationStart.required) {
        errors.push('Eine Startzeit für die Registration muss eingetragen werden.');
      }
      return errors;
    },
    registrationEndTimeErrors() {
      const errors = [];
      if (!this.$v.registrationDeadline.$dirty) return errors;
      if (!this.$v.registrationDeadline.required) {
        errors.push('Eine Zeit für das Ende der Registrierung muss eingetragen werden.');
      }
      return errors;
    },
  },
  methods: {
    getData() {
      return {
        startTime: this.data.startTime,
        endTime: this.data.endTime,
        registrationDeadline: this.data.registrationDeadline,
      };
    },
  },
  mounted() {
    this.$refs.startTimeRef.setDate(this.startTime);
    this.$refs.endTimeRef.setDate(this.endTime);
    this.$refs.registrationStartRef.setDate(this.registrationStart);
    this.$refs.registrationDeadlineRef.setDate(this.registrationDeadline);
  },
};
</script>
