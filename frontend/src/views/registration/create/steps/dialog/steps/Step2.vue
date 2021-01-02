<template>
  <v-container>
    <v-form v-model="valid">
      <v-row>
        <v-row class="mt-6">
          <span class="subtitle-1">
            Welche Essgewohnheiten hat der/die Teilnehmer*in? Vegetarisch,
            Vegan...
          </span>
        </v-row>
        <v-row>
          <v-select
            v-model="data.selectedHabit"
            :items="data.habits"
            item-text="name"
            item-value="id"
            label="Essgewohnheit wählen"
            required
            @input="validate()"
          />
        </v-row>
      </v-row>
      <v-row>
        <v-row class="mt-6">
          <span class="subtitle-1">
            Welche Allergien hat der/die Teilnehmer*in?
          </span>
        </v-row>
        <v-row>
          <v-select
            v-model="data.selectedAllergies"
            :items="data.allergies"
            item-text="name"
            item-value="id"
            label="Allergien wählen"
            multiple
            @input="validate()"
          />
        </v-row>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  props: ['isOpen'],
  components: {},
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
  computed: {},
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
