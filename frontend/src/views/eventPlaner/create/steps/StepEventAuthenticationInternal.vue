<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Du hast dich für eine Rechtemanagement mit Email Adressen entschieden!
            Jeder der Zugriff auf die Interna deines Events bekommen soll, muss hier mit seiner
            Email Adresse aufgeführt werden.
          <br/>
          <i>(Jede geschriebene E-Mail-Adresse muss mit Enter bestätigt werden!)</i>
        </span>
      </v-row>
      <v-row>
        <v-combobox
          :error-messages="contactsErrors"
          v-model="contacts"
          label="Emailadressen der Planenden"
          multiple
          required
          small-chips
          deletable-chips
          chips
        />
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required, email } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';

export default {
  name: 'StepEventAuthenticationInternal',
  header: 'DPV IDM',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    contacts: [],
  }),
  validations: {
    contacts: {
      $each: {
        required,
        email,
      },
    },
  },
  computed: {
    contactsErrors() {
      const errors = [];
      if (!this.$v.contacts.$dirty) return errors;
      if (!this.$v.contacts.required) {
        errors.push('Es muss mindestens eine Ansprechperson angegeben werden.');
      }
      if (this.$v.contacts.$each.$anyError) {
        errors.push('Es müssen gültige E-Mail-Adressen angegeben werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
      store.commit('createEvent/setResponsiblePersons', this.contacts);
    },
  },
  mounted() {
    this.contacts = this.event.responsiblePersons;
  },
};
</script>
