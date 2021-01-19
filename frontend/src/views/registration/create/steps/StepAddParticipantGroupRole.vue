<template>
  <v-form ref="formParticipantGroupRole" v-model="valid">
    <v-container>
      <span>
        Unser Lagerplatz oder Heim hat eine Möglichkeit zum Kochen <br />
        (Herd/Feuerstelle) ausreichend Toiletten (Dixi/ WC) fließend Wasser.
      </span>
      <role-picker />
    </v-container>
    <v-divider class="my-3" />

    <prev-next-buttons
      :position="position"
      :max-pos="maxPos"
      @nextStep="nextStep()"
      @prevStep="prevStep"
      @submitStep="submitStep()"
    />
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
import RolePicker from '../components/RolePicker..vue';

export default {
  name: 'StepAddParticipantGroupRole',
  displayName: 'Teilnehmer_innen Rolle',

  components: {
    RolePicker,
    PrevNextButtons,
  },
  props: ['position', 'maxPos'],
  data: () => ({
    valid: true,
    displayName: 'Essen',
  }),
  validations: {},
  methods: {
    validate() {},
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }

      this.addMeatEaters();
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    addMeatEaters() {
      this.$emit('nextStep');
    },
  },
};
</script>

<style scoped>
</style>
