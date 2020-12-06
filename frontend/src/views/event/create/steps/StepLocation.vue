<template>
  <v-form
    ref="formLocation"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-4">
        <span class="subtitle-1">
          Trage hier den Namen von dem Ort ein. <br>
        </span>
      </v-row>
      <v-row class="ma-4">
        <b>TODO</b>
      </v-row>

      <v-divider class="my-2"/>
      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepLocation',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    valid: true,
    data: {},
  }),
  methods: {
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.$refs.formLocation.validate()) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      if (!this.$refs.formLocation.validate()) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        location_id: '1',
      };
    },
  },
};
</script>
