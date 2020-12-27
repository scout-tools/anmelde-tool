<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p>
            Ich möchte mich zur Fahrt xxx anmelden.
            Ich bin von meinem Stamm bevollmächtigt ihn hier verbindlich Anmelden zu dürfen.
          </p>
        </span>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="`Ich Stimme zu`"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
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
      checkbox1: false,
      name: '',
      description: '',
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
  },
  methods: {
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
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