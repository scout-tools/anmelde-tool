<template>
  <div>
    <v-row justify="center" v-if="registrationLevel">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Einladungscode</v-card-title>
          <v-card-text>
            <div class="ma-2">
              <p class="ma-0">
                Hast du keinen Code bekommen? Schaue nochmal in der Einladung.
                Falls du nichts findest, melde dich beim Veranstalter, deiner
                Bundesführung oder bei:
                <a href="mailto:support@anmelde-tool.de">
                  support@anmelde-tool.de
                </a>
              </p>
              <p class="mt-4">
                Bevor deine Anmeldung verbindlich ist, musst du sie im letzten
                Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang
                zu jedem Zeitpunkt abbrechen und später fortsetzen. Deine Daten
                kannst du bis zum Anmeldeschluss verändern.
              </p>
            </div>
            <v-container>
              <v-row>
                <template v-for="(field, i) in fields">
                  <BaseField
                      :key="i"
                      :field="field"
                      v-model="data[field.techName]"
                      :valdiationObj="$v"
                      @keydownEnter="onConfirmClicked"
                      :ref="`baseField_${i}`"/>
                </template>
                <v-tooltip bottom v-if="registrationLevelId === 6">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        icon
                        v-bind="attrs"
                        v-on="on"
                        class="mt-6"
                        @click="onCreateScoutHierarchyClicked">
                      <v-icon fab color="primary">
                        mdi-plus
                      </v-icon>
                    </v-btn>
                  </template>
                  <span>Gruppe Hinzufügen</span>
                </v-tooltip>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer/>
            <v-btn color="grey darken-1" text @click="cancel()"> Zurück</v-btn>
            <v-btn color="success" text @click="onConfirmClicked">
              Anmeldung starten
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
    <v-snackbar v-model="showError" color="error" y="top">
      {{ errorMessage }}
    </v-snackbar>
    <CreateScoutHierarchyModal
        ref="createScoutHierarchyModal"
        @created="onCreateScoutHierarchyCreated"/>
  </div>
</template>

<script>
import axios from 'axios';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';
import { required } from 'vuelidate/lib/validators';
import CreateScoutHierarchyModal from '@/views/event/components/CreateScoutHierarchyModal.vue';

export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    dialog: false,
    showError: false,
    errorMessage: false,
    timeout: 3000,
    data: {
      scoutOrganisation: null,
      invitationCode: '',
    },
    registrationLevel: null,
  }),
  components: {
    CreateScoutHierarchyModal,
    BaseField,
  },
  mixins: [
    apiCallsMixin,
  ],
  methods: {
    onConfirmClicked() {
      this.onCreateRegistrationClicked();
    },
    show(item, single, registrationLevel) {
      this.registrationLevel = registrationLevel;
      this.single = single;
      this.item = item;
      this.dialog = true;
      this.refreshBaseFields();
    },
    cancel() {
      this.$v.$reset();
      this.registrationLevel = null;
      this.item = null;
      this.showError = false;
      this.errorMessage = '';
      this.dialog = false;
    },
    onCreateRegistrationClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.createRegistration();
    },
    createRegistration() {
      axios
        .post(`${this.API_URL}/event/registration/`, {
          eventCode: this.data.invitationCode,
          event: this.item.id,
          single: this.single,
          scoutOrganisation: this.data.scoutOrganisation,
        })
        .then((response) => {
          this.$router.push({
            name: 'registrationEdit',
            params: {
              id: response.data.id,
            },
          });
        })
        .catch((error) => {
          console.log(error);
          this.showError = true;
          this.errorMessage = error.response.data.detail;
        });
    },
    onCreateScoutHierarchyClicked() {
      this.$refs.createScoutHierarchyModal.show();
    },
    onCreateScoutHierarchyCreated(value) {
      this.data.scoutOrganisation = value.id;
      this.refreshBaseFields();
    },
    refreshBaseFields() {
      this.$nextTick(() => {
        for (let i = 0; i < this.fields.length; i += 1) {
          const ref = this.$refs[`baseField_${i}`];
          ref[0]?.refresh();
        }
      });
    },
  },
  validations: {
    data: {
      invitationCode: {
        required,
      },
      scoutOrganisation: {
        required,
      },
    },
  },
  computed: {
    registrationLevelId() {
      if (this.registrationLevel) {
        return this.registrationLevel.id;
      }
      return 5;
    },
    hierarchyName() {
      if (this.registrationLevel) {
        if (this.registrationLevel.id === 6) {
          return 'Ich melde meine Gruppe an.';
        }
        if ([2, 3, 4].includes(this.registrationLevel.id)) {
          return `Ich melde meine ${this.registrationLevel.name} an.`;
        }
      }
      return 'Ich melde meinen Stamm an.';
    },
    fields() {
      return [
        {
          name: 'Code aus der Einladung',
          techName: 'invitationCode',
          tooltip: 'Der Code steht im Einladungsschreiben.',
          icon: 'mdi-lock',
          fieldType: 'textfield',
          default: '',
          cols: 12,
        },
        {
          name: this.hierarchyName,
          techName: 'scoutOrganisation',
          tooltip: '',
          icon: 'mdi-account-group',
          lookupPath: `/event/registration-scouthierarchy/?level=${this.registrationLevelId}`,
          lookupListDisplay: ['name'],
          mandatory: true,
          fieldType: 'refDropdown',
          default: '',
          cols: this.registrationLevelId === 6 ? 10 : 12,
          value: this.data.scoutOrganisation,
        },
      ];
    },
  },
};
</script>
