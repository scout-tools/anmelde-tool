<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row>
        <span class="text-left subtitle-1">
          <p>Willkommen bei der <b> Aktionserstellung </b>.</p>
          Viele Pfadfinder_innen und Pfadfinder freuen sich schon auf deine
          Aktion. Im folgenden führen wir dich durch {{ maxPos }} kleine
          Schritte. Viel Spaß!
        </span>
      </v-row>
      <v-row>
        <span class="subtitle-1">
          Gib deiner Aktion eine passende Überschrift.
        </span>
      </v-row>
      <v-row>
        <v-text-field
          v-model="data.name"
          :counter="20"
          :error-messages="nameErrors"
          label="Name der Aktion"
          required
          @input="$v.data.name.$touch()"
          @blur="$v.data.name.$touch()"
        />
      </v-row>
      <v-row>
        <v-text-field
          v-model="data.description"
          :counter="100"
          :error-messages="descriptionErrors"
          label="Beschreibung der Aktion"
          required
          @input="$v.data.description.$touch()"
          @blur="$v.data.description.$touch()"
        />
      </v-row>

      <v-row v-if="false">
      <v-divider class="my-3" />
        <ckeditor
          :editor="ckeditor.editor"
          v-model="ckeditor.editorData"
          :config="ckeditor.editorConfig"
        ></ckeditor>
      </v-row>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep()"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required, maxLength } from 'vuelidate/lib/validators';
import { stepMixin } from '@/mixins/stepMixin';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import '@ckeditor/ckeditor5-build-classic/build/translations/de';

import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos', 'data'],
  components: {
    PrevNextButtons,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    ckeditor: {
      editor: ClassicEditor,
      editorData: '<p>Content of the editor.</p>',
      editorConfig: {
        language: 'de',
      },
    },
  }),
  validations: {
    data: {
      name: {
        required,
        maxLength: maxLength(20),
      },
      description: {
        required,
        maxLength: maxLength(100),
      },
    },
  },
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.data.name.$dirty) return errors;
      if (!this.$v.data.name.required) {
        errors.push('Veranstaltungsname ist notwendig.');
      }
      if (!this.$v.data.name.maxLength) {
        errors.push('Veranstaltungsname muss kürzer als 20 Zeichen sein.');
      }
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.data.description.$dirty) return errors;
      if (!this.$v.data.description.required) {
        errors.push('Beschreibung ist notwendig.');
      }
      if (!this.$v.data.description.maxLength) {
        errors.push('Beschreibung muss kürzer als 100 Zeichen sein.');
      }
      return errors;
    },
  },
  methods: {
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
  },
};
</script>
