<template>
  <v-form ref="StepVisibility" v-model="valid">
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
          <v-switch label="Sichtbar" v-model="isPublic"></v-switch>
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
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';

import PrevNextButton from '@/components/buttons/PrevNextButton.vue';

export default {
  name: 'StepVisibility',
  header: 'Sichtbarkeit',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isPublic: false,
  }),
  validations: {
    data: {
      isPublic: {
        required,
      },
    },
  },
  computed: {
    invitationCodeErrors() {
      const errors = [];
      if (!this.$v.data.isPublic.$dirty) return errors;
      if (!this.$v.data.isPublic.required) {
        errors.push(
          'Der Einladungscode muss aus Zahlen und Buchstaben bestehen,',
        );
      }
      return errors;
    },
  },
  methods: {
    getData() {
      return {
        isPublic: this.data.isPublic,
      };
    },
  },
};
</script>
