<template>
  <v-form ref="forStartEndDeadline" v-model="valid">
    <v-container>
      <v-row class="my-6">
        <span class="subtitle-1"> Zeitraum der Aktion. </span>
      </v-row>
      <v-row>
        <template v-for="(field, i) in fields">
          <BaseField
            :key="i"
            :field="field"
            v-model="data[field.techName]"
            :valdiationObj="$v"
          />
        </template>
      </v-row>
      <v-divider class="my-2" />
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
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  name: 'StepStartEndDeadline',
  header: 'Daten und Uhrzeit',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
    BaseField,
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      valid: true,
      data: {
        startDate: null,
        endDate: null,
        registrationDeadline: null,
        registrationStart: null,
        lastPossibleUpdate: null,
      },
      fields: [
        {
          name: 'Start',
          techName: 'startDate',
          tooltip: '123',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Ende',
          techName: 'endDate',
          tooltip: '123',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Anmeldestart',
          techName: 'registrationStart',
          tooltip: '123',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Anmeldeende',
          techName: 'registrationDeadline',
          tooltip: '123',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
        {
          name: 'Letze Änderung',
          techName: 'lastPossibleUpdate',
          tooltip: '123',
          icon: 'mdi-account-circle',
          mandatory: true,
          fieldType: 'datetime',
          default: '',
          cols: 12,
        },
      ],
    };
  },
  ...mapGetters({
    event: 'createEvent/event',
  }),
  mixins: [stepMixin, apiCallsMixin],
  validations: {
    data: {
      startDate: {
        required,
      },
      endDate: {
        required,
      },
      registrationStart: {
        required,
      },
      registrationDeadline: {
        required,
      },
      lastPossibleUpdate: {
        required,
      },
    },
  },
  methods: {
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message:
            'Deine eingegeben Daten scheinen nicht gültig zu sein, bitte überprüfe dies noch einmal',
          color: 'error',
        });
      } else {
        store.commit('createEvent/setEventAttribute', {
          prop: 'registrationDeadline',
          value: this.data.registrationDeadline,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'registrationStart',
          value: this.data.registrationStart,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'startDate',
          value: this.data.startDates,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'lastPossibleUpdate',
          value: this.data.lastPossibleUpdate,
        });
        store.commit('createEvent/setEventAttribute', {
          prop: 'endDate',
          value: this.data.endDate,
        });
      }
    },
  },
  created() {
    console.log('this.event');
    console.log(this.event);
    this.data.startDate = this.$moment(this.event.startDate).toDate();
    this.data.endDate = this.$moment(this.event.endDate).toDate();
    this.data.registrationDeadline = this.$moment(
      this.event.registrationDeadline,
    ).toDate();
    this.data.registrationStart = this.$moment(this.event.registrationStart).toDate();
    this.data.lastPossibleUpdate = this.$moment(this.event.lastPossibleUpdate).toDate();
  },
};
</script>
