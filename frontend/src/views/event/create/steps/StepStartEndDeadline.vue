<template>
  <v-form
    ref="forStartEndDeadline"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-2">
      <span class="subtitle-1">
        Startdatum deiner Aktion.
      </span>
      </v-row>
      <v-row class="ma-4">
        <v-datetime-picker
          v-model="data.startTime"
          label="Start der Aktion"
          :time-picker-props="{format: '24hr'}"
          @input="validate()"
        />
      </v-row>
      <v-row class="ma-4">
        <v-datetime-picker
          v-model="data.endTime"
          label="Ende der Aktion"
          :time-picker-props="{format: '24hr'}"
          @input="validate()"
        />
      </v-row>
      <v-row class="ma-4">
        <v-datetime-picker
          v-model="data.deadline"
          label="Anmeldeschluss"
          :time-picker-props="{format: '24hr'}"
          @input="validate()"
        />
      </v-row>

      <v-divider class="my-2"/>
      <!--      TODO Mitteilung, was den Error wirft -->
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      startTime: null,
      endTime: null,
      deadline: null,
    },
  }),
  methods: {
    validate() {
      this.valid = !!this.data.startTime && !!this.data.endTime && !!this.data.deadline;
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
      if (!this.$refs.formStartEndDeadline.validate()) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
