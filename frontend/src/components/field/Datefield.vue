<template>
  <v-text-field
    :value="value"
    @input="onDateInputChanged"
    label="Geburtsdatum"
  ></v-text-field>
</template>

<script>
import moment from 'moment'; // eslint-disable-line

export default {
  props: {
    value: {
      default: null,
    },
  },
  data() {
    return {
      dateFormat: '',
    };
  },
  methods: {
    onDateInputChanged(value) {
      const newDate = moment(value);
      if (newDate.isValid()) {
        this.dateFormat = newDate.format('LL');
        this.onInputChanged(value);
      }
    },
    onInputChanged(value) {
      this.$emit('input', value);
    },
  },
  created() {},
};
</script>
