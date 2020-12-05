<template>
  <v-form
    ref="formNameBeschreibung"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-2">
      <span class="text-left subtitle-1">
        Willkommen bei der <b> Aktionserstellung </b>. <br>
        <br>
        Viele Pfadfinder freuen sich
        schon auf deine Aktion. Im folgenden führen wir dich durch XX kleine
        Schritte. Viel Spaß!
      </span>
      </v-row>
      <v-divider class="text-left ma-5"/>
      <v-row class="mt-6 ml-2">
      <span class="subtitle-1">
        Gib deiner Aktion eine passende Überschrift.
      </span>
      </v-row>
      <v-row class="ma-4">
        <v-text-field
          outlined
          autofocus
          :counter="40"
          :rules="rules.title"
          label="Name der Aktion"
          v-model="data.title"
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
      title: '',
      materialArray: [],
      isPrepairationNeeded: false,
    },
    rules: {
      title: [
        (v) => !!v || 'Überschrift ist erforderlich.',
        (v) => (v && v.length >= 10) || 'Die Überschrift ist zu kurz.',
        (v) => (v && v.length <= 40) || 'Die Überschtift ist zu lang.',
      ],
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
      if (!this.$refs.formNameBeschreibung.validate()) {
        return;
      }
      this.$emit('nextStep');
    },
  },
};
</script>

<style scoped>

</style>
