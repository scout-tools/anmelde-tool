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
          v-model="name"
          :counter="20"
          :error-messages="nameErrors"
          label="Name der Aktion"
          required
          @input="validate"
          @blur="validate"
        />
      </v-row>
      <v-row>
        <v-text-field
          v-model="description"
          :counter="100"
          :error-messages="descriptionErrors"
          label="Beschreibung der Aktion"
          required
          @input="validate"
          @blur="validate"
        />
      </v-row>

      <prev-next-button
        :valid="valid"
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required, maxLength } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import store from '@/store';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos'],
  header: 'Aktionsbeschreibung',
  components: {
    PrevNextButton,
  },
  mixins: [stepMixin, apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    name: '',
    description: '',
  }),
  validations: {
    name: {
      required,
      maxLength: maxLength(20),
    },
    description: {
      required,
      maxLength: maxLength(100),
    },
  },
  computed: {
    nameErrors() {
      const errors = [];
      if (!this.$v.name.$dirty) return errors;
      if (!this.$v.name.required) {
        errors.push('Veranstaltungsname ist notwendig.');
      }
      if (!this.$v.name.maxLength) {
        errors.push('Veranstaltungsname muss kürzer als 20 Zeichen sein.');
      }
      return errors;
    },
    descriptionErrors() {
      const errors = [];
      if (!this.$v.description.$dirty) return errors;
      if (!this.$v.description.required) {
        errors.push('Beschreibung ist notwendig.');
      }
      if (!this.$v.description.maxLength) {
        errors.push('Beschreibung muss kürzer als 100 Zeichen sein.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message: 'Deine eingegeben Daten scheinen nicht gültig zu sein, bitte überprüfe dies noch einmal',
          color: 'error',
        });
      } else {
        store.commit('createEvent/setEventName', this.name);
        store.commit('createEvent/setEventDescription', this.description);
      }
    },
  },
  mounted() {
    if (this.event.name !== 'Dummy') {
      this.name = this.event.name;
    }
    this.description = this.event.description;
  },
};
</script>
