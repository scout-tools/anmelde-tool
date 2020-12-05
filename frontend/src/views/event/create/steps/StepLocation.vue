<template>
  <v-form
    ref="formLocation"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-4">
        <span class="subtitle-1">
          Trage hier den Namen von dem Ort ein. <br>
        </span>
      </v-row>
      <v-row class="ma-4">
        <v-text-field
          outlined
          autofocus
          :counter="40"
          :rules="rules.location.name"
          label="Name des Ortes"
          v-model="data.location.name"
          required>
        </v-text-field>
      </v-row>

      <v-divider class="my-2"/>
      <prev-next-buttons :position="position" @nextStep="nextStep()" @prevStep="prevStep"/>

    </v-container>
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/PrevNextButtonsSteps.vue';

export default {
  props: ['position'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    valid: true,
    data: {
      location: {
        name: '',
      },
    },
    rules: {
      location: {
        name: [
          (v) => !!v || 'Titel ist erforderlich.',
          (v) => (v && v.length >= 10) || 'Der Titel ist zu kurz.',
          (v) => (v && v.length <= 40) || 'Der Titel ist zu lang.',
        ],
      },
    },
  }),

  computed: {
    isCreate() {
      return !this.$route.params.id;
    },
    isUpdate() {
      return !!this.$route.params.id;
    },
  },

  created() {
    if (this.$route.params.id) {
      this.data = this.$route.params;
    }
  },

  methods: {
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.$refs.formLocation.validate()) {
        return;
      }
      this.$emit('nextStep');
    },
  },
};
</script>

<style scoped>

</style>
