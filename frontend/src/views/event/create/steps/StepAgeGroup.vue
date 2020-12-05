<template>
  <v-form
    ref="formAgeGroup"
    v-model="valid"
  >
    <v-container>
      <v-row class="mt-6 ml-2">
      <span class="subtitle-1">
        Für welche Zielgruppe(n) ist deine Aktion?
      </span>
      </v-row>
      <v-row class="ma-4">
        <v-select
          v-model="selectedAgeGroups"
          :items="getItems"
          item-text="name"
          item-value="id"
          label="Zielgruppe(n) wählen"
          multiple
          outlined
          @input="validate()"
        />
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
    selectedAgeGroups: [],
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      name: '',
      description: '',
    },
  }),
  computed: {
    getItems() {
      // TODO replace with HTTP
      return [
        {
          model: 'basic.ageGroup',
          pk: 1,
          fields: {
            id: 1,
            name: 'Wölflinge',
            description: '',
          },
        },
        {
          model: 'basic.ageGroup',
          pk: 2,
          fields: {
            id: 2,
            name: 'Pfadfinder',
            description: '',
          },
        },
        {
          model: 'basic.ageGroup',
          pk: 3,
          fields: {
            id: 3,
            name: 'Rover',
            description: '',
          },
        },
      ].map((group) => ({
        id: group.fields.id,
        name: group.fields.name,
        description: group.fields.description,
      }));
    },
  },
  methods: {
    validate() {
      this.valid = this.selectedAgeGroups > 0;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      if (!this.$refs.formAgeGroup.validate()) {
        return;
      }
      this.$emit('submit');
    },
  },
};
</script>
