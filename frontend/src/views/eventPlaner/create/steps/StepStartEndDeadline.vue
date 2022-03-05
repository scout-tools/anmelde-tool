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
      <v-row>
        <v-card-text>
          Unabhängig vom Ende der Anmeldephase, kann man einstellen bis wann bereits Angemeldete
          ihre Daten verändern können. Diese veränderten Daten werden mit einem Tag versehen
          und müssen von der Lagerleitung bestätigt werden.
          Wenn es keine Möglichkeit geben soll die Daten nach dem Anmeldeende zu verändern,
          kann dieses Feld leer gelassen werden.
        </v-card-text>
        <DateTimePicker
          ref="registrationLasPossibleUpdate"
          v-model="lastPossibleUpdate"
          title="Bearbeitungsende"
          :error-messages-date="registrationEndTimeErrors"
          :error-messages-time="registrationEndTimeErrors"
        />
      </v-row>
      <v-divider class="my-2"/>
      <prev-next-button
        :valid="valid"
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>

import { required } from 'vuelidate/lib/validators';
import moment from 'moment';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';
import DateTimePicker from '@/components/picker/DateTimePicker.vue';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

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
      lastPossibleUpdate: null,
    };
  },
  mixins: [stepMixin, apiCallsMixin],
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
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message: 'Deine eingegeben Daten scheinen nicht gültig zu sein, bitte überprüfe dies noch einmal',
          color: 'error',
        });
      } else {
        store.commit('createEvent/setEventAttribute', {
          prop: 'registrationDeadline',
          value: this.registrationDeadline,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'registrationStart',
          value: this.registrationStart,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'startTime',
          value: this.startTime,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'lastPossibleUpdate',
          value: this.lastPossibleUpdate,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'endTime',
          value: this.endTime,
        });
      }
    },
  },
  mounted() {
    this.startTime = moment(this.event.startTime)
      .toDate();
    this.endTime = moment(this.event.endTime)
      .toDate();
    this.registrationDeadline = moment(this.event.registrationDeadline)
      .toDate();
    this.registrationStart = moment(this.event.registrationStart)
      .toDate();
    this.lastPossibleUpdate = moment(this.event.lastPossibleUpdate)
      .toDate();
    this.$refs.startTimeRef.setDate(this.startTime);
    this.$refs.endTimeRef.setDate(this.endTime);
    this.$refs.registrationStartRef.setDate(this.registrationStart);
    this.$refs.registrationDeadlineRef.setDate(this.registrationDeadline);
  },
};
</script>
