<template>
  <v-form
    ref="formNameDescription"
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
          :counter="20"
          :rules="rules.name"
          label="Name der Aktion"
          v-model="data.name"
          required>
        </v-text-field>
      </v-row>
      <v-row class="ma-4">
        <v-text-field
          outlined
          :counter="100"
          :rules="rules.description"
          label="Beschreibung der Aktion"
          v-model="data.description"
          required>
        </v-text-field>
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-buttons :position="position" :max-pos="maxPos" @nextStep="nextStep()"
                         @prevStep="prevStep" @submitStep="submitStep()"/>
    </v-container>
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
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
    rules: {
      name: [
        (v) => !!v || 'Titel ist erforderlich.',
        (v) => (v && v.length <= 20) || 'Der Titel ist zu lang.',
      ],
      description: [
        (v) => !!v || 'Beschreibung ist erforderlich.',
        (v) => (v && v.length <= 100) || 'Die Beschreibung ist zu lang.',
      ],
    },
  }),
  methods: {
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.$refs.formNameDescription.validate()) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      if (!this.$refs.formNameDescription.validate()) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
