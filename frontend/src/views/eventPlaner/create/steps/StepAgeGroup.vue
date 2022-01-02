<template>
  <v-form ref="formAgeGroup" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
          Für welche Zielgruppe(n) ist deine Aktion?
        </span>
      </v-row>
      <v-row>
        <v-select
          v-model="ageGroups"
          :items="ageGroupList"
          :error-messages="ageGroupsErrors"
          item-text="name"
          item-value="id"
          label="Zielgruppe(n) wählen"
          multiple
          required
          @input="validate()"/>
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
        @ignore="onIngoredClicked"
        @update="postData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';

export default {
  name: 'StepAgeGroup',
  header: 'Zielgruppe',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    items: [],
    ageGroupList: [],
    API_URL: process.env.VUE_APP_API,
    valid: true,
    ageGroups: [],
  }),
  validations: {
    ageGroups: {
      required,
    },
  },
  computed: {
    ageGroupsErrors() {
      const errors = [];
      if (!this.$v.ageGroups.$dirty) return errors;
      if (!this.$v.ageGroups.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
  },
  methods: {
    async getAvailableAgeGroups() {
      const result = await axios.get(`${this.API_URL}/basic/age-group/`);
      this.ageGroupList = result.data;
    },
    postData() {

    },
  },
  created() {
    this.getAvailableAgeGroups();
  },
};
</script>
