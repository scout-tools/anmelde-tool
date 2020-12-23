<template>
  <v-form
    ref="formNameDescription"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-2">
      <span class="text-left subtitle-1">
        <p>
        Willkommen bei der <b> Aktionserstellung </b>.
        </p>
        Viele Pfadfinder freuen sich
        schon auf deine Aktion. Im folgenden führen wir dich durch {{ maxPos }} kleine
        Schritte. Viel Spaß!
      </span>
      </v-row>
      <v-divider class="text-left my-2"/>
      <v-row class="mb-6">
      <span class="subtitle-1">
        Gib deiner Aktion eine passende Überschrift.
      </span>
      </v-row>
      <v-row>
        <v-text-field
          v-model="data.name"
          :counter="20"
          :error-messages="nameErrors"
          label="Name der Aktion"
          required
          @input="$v.data.name.$touch()"
          @blur="$v.data.name.$touch()"> <!-- TODO: Blur oder Autofocus => Prio? -->
        </v-text-field>
      </v-row>
      <v-row>
        <v-text-field
          v-model="data.description"
          :counter="100"
          :error-messages="descriptionErrors"
          label="Beschreibung der Aktion"
          required
          @input="$v.data.description.$touch()"
          @blur="$v.data.description.$touch()">
        </v-text-field>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import { required, maxLength } from 'vuelidate/lib/validators';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      name: '',
      description: '',
    },
  }),
  validations: {
    data: {
      name: {
        required,
        maxLength: maxLength(20),
      },
      description: {
        required,
        maxLength: maxLength(100),
      },
    },
  },
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.data.name.$dirty) return errors;
      if (!this.$v.data.name.required) {
        errors.push('Name is required.');
      }
      if (!this.$v.data.name.maxLength) {
        errors.push('Name must be at most 20 characters long');
      }
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.data.description.$dirty) return errors;
      if (!this.$v.data.description.required) {
        errors.push('description is required.');
      }
      if (!this.$v.data.description.maxLength) {
        errors.push('description must be at most 100 characters long');
      }
      return errors;
    },
  },
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$error;
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
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
  },
};
</script>
