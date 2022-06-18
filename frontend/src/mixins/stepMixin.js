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
        this.saving = false;
        return;
      }
      this.$emit('submit');
    },
    submit() {
      this.$emit('saving', true);
      this.$emit('submit');
    },
    prevStep() {
      this.$emit('saving', true);
      this.$emit('prevStep');
    },
    nextStep(force = false) {
      this.validate();
      if (!this.valid && !force) {
        this.$emit('saving', false);
        this.saving = false;
        return;
      }
      this.$emit('nextStep', force);
    },
    onSaving(state) {
      this.saving = state;
    },
    onIngoredClicked() {
      this.$emit('nextStep', true);
    },
    ignore() {
      this.$emit('saving', true);
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
      if (valObj.email === false) {
        errors.push('Muss eine richtige E-Mail-Adresse sein.');
      }
      if (valObj.allChecked === false) {
        errors.push('Es müssen allen Bedindungen zugestimmt werden.');
      }
      if (valObj.alphaNumExtendedValidator === false) {
        errors.push('Es sind nur Kleinbuchstaben, Zahlen und Bindestriche erlaubt.');
      }
      if (valObj.alphaNum === false) {
        errors.push('Es sind nur Buchstaben und Zahlen erlaubt.');
      }
      if (valObj.numeric === false) {
        errors.push('Es sind nur Zahlen erlaubt.');
      }
      if (valObj.integer === false) {
        errors.push('Es sind nur natürliche Zahlen erlaubt.');
      }
      if (valObj.url === false) {
        errors.push('Muss eine richtige URL sein.');
      }
      if (valObj.minDeadline === false) {
        errors.push('Der Anmeldeschluss muss nach dem Anmeldestart liegen.');
      }
      if (valObj.minLastPossibleUpdate === false) {
        errors.push('Das Letzte Änderungsdatum muss auf oder nach dem Anmeldeschluss liegen.');
      }
      if (valObj.minStartDate === false) {
        errors.push('Der Beginn der Fahrt muss auf oder nach dem Letzte Änderungsdatum liegen.');
      }
      if (valObj.minEndDate === false) {
        errors.push('Das Ende der Fahrt muss nach dem Start der Fahrt liegen.');
      }
      if (valObj.minYearRegistration === false) {
        errors.push('Der Start der Fahrt liegt zuweit in der Vergangenheit (>1 Jahr).');
      }
      if (valObj.minYearAge === false) {
        errors.push('Bisschen alt, nich?');
      }
      if (valObj.between === false) {
        const {
          min,
          max,
        } = valObj.$params.between;
        errors.push(
          `Bitte gib einen Wert zwischen ${min}€ und ${max}€ ein. Falls du mehr als ${max} brauchst melde dich bei der Lagerleitung.`,
        );
      }
      return errors;
    },
    updateData(isLastStep = false) {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message: 'Daten prüfen.',
          color: 'error',
        });
      } else {
        this.fields.forEach((field) => {
          setTimeout(() => {
            this.patchService(
              field.techName,
              this.data[field.techName],
              this.modulePath,
              this.event.id,
            );
          }, 75);
        });
        if (isLastStep) {
          this.$root.globalSnackbar.show({
            message: 'Daten gespeichert.',
            color: 'success',
          });
          this.$router.push({ name: 'eventPlaner' });
        }
      }
    },
  },
  computed: {
    id() {
      return this.$route.params.id;
    },
  },
};
