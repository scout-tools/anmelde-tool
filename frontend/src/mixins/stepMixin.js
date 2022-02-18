export const stepMixin = { // eslint-disable-line
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep(force = false) {
      this.validate();
      if (!this.valid && !force) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    errorMessage(field) {
      const errors = [];
      const valObj = this.$v.item[field];
      if (!valObj.$dirty) return errors;
      if (valObj.required === false) {
        errors.push('Dieses Feld ist erforderlich.');
      }
      if (valObj.minLength === false) {
        const { min } = valObj.$params.minLength;
        errors.push(`Du musst mindestens ${min} Zeichen nutzen.`);
      }
      if (valObj.maxLength === false) {
        const { max } = valObj.$params.maxLength;
        errors.push(`Du darfst maximal ${max} Zeichen nutzen.`);
      }
      if (valObj.minValue === false) {
        errors.push(`Minimal sind ${valObj.$params.minValue.min} erlaubt.`);
      }
      if (valObj.maxValue === false) {
        errors.push(`Maximal sind ${valObj.$params.maxValue.max} erlaubt.`);
      }
      if (valObj.between === false) {
        const { min, max } = valObj.$params.between;
        errors.push(`Bitte gib einen Wert zwischen ${min}€ und ${max}€ ein. Falls du mehr als ${max} brauchst melde dich bei der Lagerleitung.`);
      }
      return errors;
    },
  },
};
