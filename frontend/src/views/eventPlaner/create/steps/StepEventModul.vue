<template>
  <v-form ref="StepEventModul" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Lege für die Aktion einen 6-Stelligen Verifizierungscode fest. <br/>
          Dieser besteht aus Buchstaben und Zahlen und wird bei der Anmeldung
          mitgeschickt, damit sich die Anmelder verifizieren können, dass sie
          eingeladen wurden. <br/>
          Bei leerem Feld gibt es keinen Verifizierungscode.
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-col cols="3">
          <v-select
            v-model="eventTags"
            :items="eventTagList"
            :error-messages="eventTagsErrors"
            item-text="name"
            item-value="id"
            label="Event Tags wählen"
            multiple
            required
            @input="validate()"
          />
        </v-col>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
        @ignore="onIngoredClicked"
      />
    </v-container>
  </v-form>
</template>

<script>
import axios from 'axios';
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';

export default {
  name: 'StepEventModul',
  header: 'Module',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    eventTagList: [],
    eventTags: [],
  }),
  mixins: [stepMixin],
  validations: {
    eventTags: {
      required,
    },
  },
  computed: {
    eventTagsErrors() {
      const errors = [];
      if (!this.$v.eventTags.$dirty) return errors;
      if (!this.$v.eventTags.required) {
        errors.push('Nötig');
      }
      return errors;
    },
  },
  methods: {
    async getEventTags() {
      const result = await axios.get(`${this.API_URL}/basic/event-tag/`);
      this.eventTagList = result.data;
    },
    getData() {
      return {
        eventTags: this.eventTags,
      };
    },
  },
  created() {
    this.getEventTags();
  },
};
</script>
