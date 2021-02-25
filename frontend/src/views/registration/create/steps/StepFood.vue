<template>
  <v-form ref="formStepFood" v-model="valid">
    <v-tabs vertical class="ma-10">
      <v-tab>
        Wölflinge
      </v-tab>
      <v-tab>
        Pfadfinder_innen
      </v-tab>
      <v-tab>
        RoverInnen
      </v-tab>
      <v-tab>
        Alt-Rover
      </v-tab>

      <v-tab-item>
        <v-card flat>
          <eat-picker/>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <eat-picker/>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <eat-picker/>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <eat-picker/>
        </v-card>
      </v-tab-item>
    </v-tabs>
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
import EatPicker from '../components/EatPicker.vue';

export default {
  components: {
    EatPicker,
    PrevNextButtons,
  },
  name: 'StepFood',
  displayName: 'Essgewohnheiten',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'scoutOrganisation',
  ],
  data: () => ({
    valid: true,
    displayName: 'Essgewohnheiten',
  }),
  validations: {},
  methods: {
    validate() {
    },
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
    beforeTabShow() {
    },
  },
};
</script>

<style scoped>

</style>
