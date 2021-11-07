<template>
  <v-container fluid>
    <v-row>
      <v-col cols="6">
        <v-menu
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          :return-value.sync="date"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="date"
              :label="`Datum für ${title}`"
              prepend-icon="mdi-calendar"
              readonly
              :error-message="errorMessagesDate"
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker v-model="date" @change="save" no-title scrollable>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menu = false">
              Abbrechen
            </v-btn>
            <v-btn text color="primary" @click="$refs.menu.save(date)">
              OK
            </v-btn>
          </v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="6">
        <v-menu
          ref="menu2"
          v-model="menu2"
          :close-on-content-click="false"
          :nudge-right="40"
          :return-value.sync="time"
          transition="scale-transition"
          offset-y
          max-width="290px"
          min-width="290px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="time"
              :label="`Zeit für ${title}`"
              prepend-icon="mdi-clock-time-four-outline"
              :error-message="errorMessagesTime"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-time-picker
            v-if="menu2"
            v-model="time"
            full-width
            format="24hr"
            :allowed-minutes="[0, 15, 30, 45]"
            @click:minute="$refs.menu2.save(time)"
            @change="save"
          ></v-time-picker>
        </v-menu>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import moment from 'moment';

import { required } from 'vuelidate/lib/validators';

export default {
  data: () => ({
    menu: false,
    menu2: false,
    date: '',
    time: '',
  }),
  validations: {
    date: {
      required,
    },
    time: {
      required,
    },
  },
  props: {
    value: {
      type: Date,
    },
    title: {
      type: String,
    },
    errorMessagesDate: {
      type: Array,
    },
    errorMessagesTime: {
      type: Array,
    },
  },
  methods: {
    save() {
      this.$emit(
        'input',
        moment(`${this.date} ${this.time}`, 'YYYY-MM-DD hh:mm').toDate(),
      );
    },
    setDate(date) {
      this.date = date ? moment(date).format('YYYY-MM-DD') : null;
      this.time = date ? moment(date).format('hh:mm') : null;
    },
  },
};
</script>

<style>
</style>
