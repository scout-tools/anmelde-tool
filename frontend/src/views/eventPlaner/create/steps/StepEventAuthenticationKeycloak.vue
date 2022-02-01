<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Du hast dich für eine Rechtemanagement mit dem DPV IDM entschieden, cool!
            So kann jeder der z.b. Zugriff im Wiki oder in der Cloud auf dein Event hat, auch hier
            Einsicht in deine Aktion bekommen.
          <br/>
           Wähle dazu einfach aus der Liste die entsprechende IDM Gruppe aus.
          <br/>
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-select
          v-model="contact"
          :items="groups"
          :error-messages="contactsErrors"
          item-text="name"
          item-value="id"
          label="Gruppe auswählen "
          required
          @input="validate"
        />
      </v-row>
      <v-row>
        Ist die Lagerleitung in einer seperaten Gruppe eingeteilt?
        Wenn nicht, können alle aus dem Planungsteam alle Einstellungen vornehmen.
      </v-row>
      <v-row>
        <v-select
          v-model="adminContact"
          :items="groups"
          item-text="name"
          item-value="id"
          label="Lagerleitungsgruppe auswählen "
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
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import { mapGetters } from 'vuex';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';

export default {
  name: 'StepEventAuthenticationKeycloak',
  header: 'DPV IDM',
  props: ['position', 'maxPos'],
  mixins: [stepMixin],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    contact: null,
    adminContact: null,
    groups: [],
  }),
  validations: {
    contact: {
      required,
    },
  },
  computed: {
    contactsErrors() {
      const errors = [];
      if (!this.$v.contact.$dirty) return errors;
      if (!this.$v.contact.required) {
        errors.push('Es muss mindestens eine Gruppe ausgewählt werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    async getGroups() {
      const url = `${this.API_URL}/auth/groups/`;
      axios.get(url)
        .then((success) => {
          this.groups = success.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    updateData() {
      store.commit('createEvent/setKeycloakGroup', this.contact);
      store.commit('createEvent/setKeycloakAdminGroup', this.adminContact);
    },
  },
  created() {
    this.adminContact = this.event.keycloakAdminPath;
    this.contact = this.event.keycloakPath;
    this.getGroups();
  },
};
</script>
