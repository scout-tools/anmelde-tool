export default {
  methods: {
    validate() {
      try {
        this.$v.$touch();
        this.valid = !this.$v.$error;
      } catch (err) {
        this.valid = true;
      }
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
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
