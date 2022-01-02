export default {
  // eslint-disable-line
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    beforeTabShow() {
      // this.onRefresh();
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
    onIngoredClicked() {
      this.$emit('nextStep');
    },
  },
};
