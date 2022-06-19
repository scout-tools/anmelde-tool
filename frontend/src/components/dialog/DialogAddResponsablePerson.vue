<template>
  <v-dialog v-model="active" transition="dialog-top-transition" max-width="800">
    <v-card>
      <v-toolbar dark color="primary">
        <v-btn icon dark @click="active = false">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Neuen Verantwortlicheren hinzufügen</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
      <v-container>
        <v-row class="ma-4">
          Diese Person hat zukünfigt vollen Zugriff auf deine Anmeldung.
        </v-row>
        <v-row>
          <template v-for="(field, i) in dialogMeta.fields">
            <BaseField
              :key="i"
              :field="field"
              v-model="data[field.techName]"
              :valdiationObj="$v"
            />
          </template>
        </v-row>
        <v-divider class="my-2"/>
        <v-row class="ma-1">
          <v-spacer></v-spacer>
          <v-btn color="success" @click="onClickOkay">Diese Person berechtigen</v-btn>
        </v-row>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<script>
import BaseField from '@/components/common/BaseField.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import { required } from 'vuelidate/lib/validators';

export default {
  components: {
    BaseField,
  },
  mixins: [apiCallsMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    active: false,
    valid: true,
    edit: false,
    data: {},
  }),
  methods: {
    validate() {
      this.$v.$touch();
      this.valid = !this.$v.$anyError;
    },
    open(item) {
      this.data = item;
      this.active = true;
    },
    close() {
      this.active = false;
      this.data = {};
    },
    onClickOkay() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.patchRegService('add-reponsable', this.data.id, 'responsable_person', this.data.responsablePerson).then(() => {
        this.active = false;
      });
    },
  },
  validations: {
    data: {
      responsablePerson: {
        required,
      },
    },
  },
  computed: {
    dialogMeta() {
      return {
        fields: [
          {
            name: 'Neue Verantwortlicherer',
            techName: 'responsablePerson',
            tooltip: 'Hier kannst du jede Person hinzufügen, welche sich bereits im Anmelde-Tool registriert hat.',
            icon: 'mdi-shape',
            lookupPath: '/auth/responsables/',
            lookupListDisplay: ['scoutName', '$ - ', 'stamm'],
            mandatory: true,
            fieldType: 'responsablesField',
            default: '',
          },
        ],
      };
    },
  },
};
</script>
