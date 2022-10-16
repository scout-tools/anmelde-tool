<template>
  <v-card flat>
    <v-card-title class="text-center justify-center py-6">
      Deine Persönlichen Daten
    </v-card-title>
    <v-card-text>
      <v-container v-if="!loading">
      <v-container v-if="!isPersonConnected">
        <v-subheader class="ma-5">
          Du musst eine Person auswählen oder erstellen.</v-subheader
        >
        <v-row>
          <v-autocomplete
            clearable
            :loading="loading"
            :items="personList"
            v-model="person"
            label="Filter nach Buchoptionen"
            :item-text="getPersonText"
            item-value="id"
            no-data-text="Keine Buchoptionen gefunden."
          />
        </v-row>
        <v-row>
          <v-btn v-if="!isPersonSelected" class="ma-2" @click="newItem" color="success">
            Neue Person hinzufügen
          </v-btn>
          <v-btn v-if="isPersonSelected" class="ma-2" @click="onConnectPerson">
            Ich bin diese Person
          </v-btn>
        </v-row>
      </v-container>
      <v-container v-else>
        <v-row>
          <template v-for="(field, i) in dialogMeta.fields">
            <BaseField
              :key="i"
              :field="field"
              v-model="data[field.techName]"
            />
          </template>
        </v-row>
        <v-row>
          <v-btn v-if="!person" class="ma-2" @click="editItem" color="success">
            <v-icon left>mdi-pencil</v-icon>
            Meine Daten ändern
          </v-btn>
          <v-btn v-if="!person" class="ma-2" @click="onDisconnectPerson" color="error">
            <v-icon left>mdi-close</v-icon>
            Diese Person entfernen
          </v-btn>
        </v-row>
      </v-container>
      </v-container>
      <v-container v-else>
        <Circual />
      </v-container>
    </v-card-text>
    <create-modal ref="createModal" @refresh="onRefresh()" />
  </v-card>
</template>

<script>
import axios from 'axios';
import serviceMixin from '@/mixins/serviceMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import { mapGetters } from 'vuex';

import CreateModal from '@/views/settings/person/CreatePerson.vue';
import BaseField from '@/components/common/BaseField.vue';
import Circual from '@/components/loading/Circual.vue';

export default {
  components: {
    CreateModal,
    BaseField,
    Circual,
  },
  mixins: [serviceMixin, apiCallsMixin],
  data() {
    return {
      person: null,
      loading: true,
      personList: [],
      personalData: null,
    };
  },
  computed: {
    ...mapGetters(['userinfo']),
    theme: {
      get() {
        return this.$store.state.preferences.theme;
      },
      set(theme) {
        this.$store.commit('setTheme', theme);
      },
    },
    isPersonConnected() {
      if (this.personalData && this.personalData.person) {
        console.log(this.personalData.person.id);
        return !!this.personalData.person.id;
      }
      return false;
    },
    isPersonSelected() {
      return !!this.person;
    },
    dialogMeta() {
      return {
        title: 'Hallo',
        excelUpload: true,
        path: 'auth/person',
        listDisplay: ['firstName', 'lastName'],
        orderBy: 'firstName',
        maxItems: null,
        minItems: 1,
        fields: [
          {
            name: 'Vorname*',
            techName: 'firstName',
            tooltip:
              'Deadnamen/Tote-Vornamen müssen nicht benutzt werden. Zweitnamen müssen nicht mit angegeben werden.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Nachname*',
            techName: 'lastName',
            tooltip: 'Trage bitte den vollständigen Nachnamen ein.',
            icon: 'mdi-card-account-details-outline',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Fahrtenname',
            techName: 'scoutName',
            tooltip: 'Trage bitte den Fahrtennamen des_der Teilnehmer_in ein.',
            icon: 'mdi-campfire',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Geburtstag*',
            techName: 'birthday',
            tooltip: 'Trage bitte das Geburtsdatum des_der Teilnehmer_in ein.',
            icon: 'mdi-calendar',
            mandatory: true,
            fieldType: 'date',
            readonly: true,
            default: '',
          },
          {
            name: 'E-Mail Adresse',
            techName: 'email',
            tooltip:
              'Trage bitte die E-Mail Adresse des_der Teilnehmer_in ein.',
            icon: 'mdi-email',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Geschlecht*',
            techName: 'gender',
            tooltip: 'Trage bitte das Geschlecht des_der Teilnehmer_in ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'localRefDropdown',
            readonly: true,
            referenceDisplay: 'name',
            referenceTable: [
              {
                name: 'weiblich',
                value: 'F',
              },
              {
                name: 'männlich',
                value: 'M',
              },
              {
                name: 'divers',
                value: 'D',
              },
              {
                name: 'Keine Angabe',
                value: 'N',
              },
            ],
          },
          {
            name: 'Straße und Hausnummer*',
            techName: 'address',
            tooltip: 'Trage bitte Straße und Hausnummer ein.',
            icon: 'mdi-home',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Postleitzahl/Ort*',
            techName: 'zipCode',
            tooltip:
              'Trage bitte den Wohnort oder die Postleitzahl des Wohnortes aus.',
            icon: 'mdi-city',
            mandatory: true,
            fieldType: 'zipField',
            default: '',
            lookupListDisplay: ['zipCode', 'city'],
            readonly: true,
          },
          {
            name: 'Telefonnummer',
            techName: 'phoneNumber',
            tooltip:
              'Trage bitte eine Mobil- oder Festnetznummer ein unter der der_die Teilnehmer_in oder die Erziehungsberechtigten nach der Fahrt erreichbar sind.',
            icon: 'mdi-phone',
            mandatory: true,
            fieldType: 'textfield',
            readonly: true,
            default: '',
          },
          {
            name: 'Essenbesonderheiten',
            techName: 'eatHabits',
            tooltip: 'Weitere Besonderheiten können einfach eingetippt werden.',
            icon: 'mdi-food',
            mandatory: true,
            lookupPath: '/basic/eat-habits/',
            lookupListDisplay: ['name'],
            fieldType: 'refCombo',
            readonly: true,
            default: '',
          },
          {
            name: 'Position*',
            techName: 'leader',
            tooltip:
              'Wenn die Person eine Führungsposition ausführt, bitte angeben',
            icon: 'mdi-office-building ',
            mandatory: false,
            lookupPath: '/event/choices/leader-types/',
            lookupListDisplay: ['name'],
            fieldType: 'enumCombo',
            multiple: false,
            readonly: true,
            default: 'N',
          },
        ],
      };
    },
    data() {
      return this.personalData.person;
    },
  },
  methods: {
    newItem() {
      this.$refs.createModal.openDialog();
    },
    editItem() {
      this.$refs.createModal.openDialogEdit(this.personalData.person);
    },
    deleteItem() {
      this.$refs.createModal.openDialog();
    },
    getPersonText(item) {
      return `${item.firstName} ${item.lastName}`;
    },
    convertEnum(list) {
      return list.map((x) => { // eslint-disable-line
        return {
          value: x[0],
          name: x[1],
        };
      });
    },
    onConnectPerson() {
      this.loading = true;
      const path = `${this.API_URL}/auth/person-connect/`;
      axios
        .post(path, {
          person: this.person,
        })
        .then((response) => {
          console.log(response);
          this.getPeronalData();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    onDisconnectPerson() {
      this.loading = true;
      const path = `${this.API_URL}/auth/person-connect/`;
      axios
        .delete(path)
        .then((response) => {
          console.log(response);
          this.getPeronalData();
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getData() {
      this.loading = true;
      Promise.all([this.getPersons()])
        .then((values) => {
          this.personList = values[0].data;
          this.getPeronalData();
        })
        .catch((err) => {
          this.$root.globalSnackbar.show({
            message: err.data,
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getPeronalData() {
      const path = `${this.API_URL}/auth/personal-data/`;
      axios
        .get(path)
        .then((res) => {
          this.personalData = res.data;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message:
              'Es gab einen Fehler beim runterladen deiner Daten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
