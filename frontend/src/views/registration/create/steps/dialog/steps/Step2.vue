<template>
  <v-container>
    <v-form v-model="valid">
      <v-row>
          <eat-field/>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

import EatField from '@/components/field/EatField.vue';

export default {
  props: ['isOpen'],
  components: {
    EatField,
  },
  computed: {
    ...mapGetters(['eatHabitTypeMapping']),
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    data: {
      habits: ['fleisch', 'vegetarisch', 'vegan'],
      allergies: ['laktose', 'glucose'],
      selectedHabit: 'fleisch',
      selectedAllergies: [],
    },
    showError: false,
    showSuccess: false,
    timeout: 7000,
  }),
  validations: {},
  methods: {
    onClickOk() {
      this.active = false;
    },
    onClickCancel() {
      this.active = false;
    },
    openDialog() {
      this.active = true;
    },
    closeDialog() {
      this.active = false;
      this.$v.$reset();
      Object.keys(this.data).forEach((key) => {
        this.data[key] = '';
      });
      this.$emit('close');
    },
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    onClickOkay() {
      this.validate();
      if (this.valid) {
        try {
          this.callCreateEventLocationPost();
          this.closeDialog();
        } catch (e) {
          console.log(e);
          this.showError = true;
        }
      }
    },
    async callCreateEventLocationPost() {
      await axios.post(`${this.API_URL}basic/event-location/`, this.data);
    },
  },
};
</script>
