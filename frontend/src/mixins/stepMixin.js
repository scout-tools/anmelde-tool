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
    submit() {
      this.$emit('submit');
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep(force = false) {
      this.validate();
      if (!this.valid && !force) {
        return;
      }
      this.$emit('nextStep', force);
    },
    onIngoredClicked() {
      this.$emit('nextStep', true);
    },
    ignore() {
      this.$emit('ignore', true);
    },
    errorMessage(field, valdiationObj) {
      const errors = [];
      if (!valdiationObj.data[field]) {
        return errors;
      }
      const valObj = valdiationObj.data[field];
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
      if (valObj.allChecked === false) {
        errors.push('Es müssen allen Bedindungen zugestimmt werden.');
      }
      if (valObj.between === false) {
        const { min, max } = valObj.$params.between;
        errors.push(
          `Bitte gib einen Wert zwischen ${min}€ und ${max}€ ein. Falls du mehr als ${max} brauchst melde dich bei der Lagerleitung.`,
        );
      }
      return errors;
    },
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message: 'Daten prüfen.',
          color: 'error',
        });
      } else {
        this.fields.forEach((field) => {
          this.patchService(field.techName, this.data[field.techName], this.modulePath);
        });
      }
    },
  },
  computed: {
    id() {
      return this.$route.params.id;
    },
  },
};
