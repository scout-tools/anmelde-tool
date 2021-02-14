<template>
  <v-autocomplete
    v-model="value"
    :items="zipCodeMapping"
    :search-input.sync="search"
    :item-text="customText"
    required
    :error-messages="zipCodeErrors"
    item-value="id"
    label="Stadt / Postleitzahl"
    placeholder="Wähle Stadt oder Postleitzahl"
    prepend-icon="mdi-city"
    @change="onInputChange"
    @input="$v.value.$touch()"
    @blur="$v.value.$touch()"
  >
    <template slot="append">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon color="success" dark v-bind="attrs" v-on="on">
            mdi-help-circle-outline
          </v-icon>
        </template>
        <span>
          {{ toolTip }}
        </span>
      </v-tooltip>
    </template>
  </v-autocomplete>
</template>

<script>
import { mapGetters } from 'vuex';
import { required } from 'vuelidate/lib/validators';

export default {
  prop: ['value'],

  data: () => ({
    API_URL: process.env.VUE_APP_API,
    entries: [],
    isLoading: false,
    value: null,
    search: null,
    toolTip: 'Trage bitte den Wohnort oder die Postleitzahl'
      + 'des Wohnorts ein und wähle die richtige Option aus.',
  }),
  validations: {
    value: {
      required,
    },
  },
  methods: {
    customText: (item) => `${item.zipCode} — ${item.city}`,
    onInputChange() {
      this.$v.value.$touch();
      this.$emit('input', this.value);
    },
    setValue(value) {
      this.value = value;
    },
  },
  computed: {
    ...mapGetters(['zipCodeMapping']),
    zipCodeErrors() {
      const errors = [];
      if (!this.$v.value.$dirty) return errors;
      if (!this.$v.value.required) {
        errors.push('Stadt ist erforderlich.');
      }
      return errors;
    },
  },
};
</script>
