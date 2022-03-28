<template>
  <v-card flat>
    <v-card-title class="text-center justify-center py-6">
      Hier kannst du deinen persönlichen Account anpassen.
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-subheader class="ma-5">
          Hier musst du deine persönlichen Daten angeben. Deine
          Stammes-Zugehörigkeit sowie deinen Fahrtenname sind wichtig, damit du
          dich oder deinen Stamm bei Fahrten anmelden kannst. Fülle die Felder
          deswegen unbedingt aus. Die Handynummer ist freiwillig und hilft dich
          zu kontaktieren.
        </v-subheader>
        <v-row>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="scoutName"
              label="Fahrtenname*"
              prepend-icon="mdi-account-circle"
              @change="updateData"
              :error-messages="scoutNameErrors"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="info" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ tooltip.scoutName }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              readonly
              disabled
              filled
              v-model="email"
              label="E-Mail Adresse*"
              prepend-icon="mdi-email"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="info" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ tooltip.email }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              readonly
              filled
              v-model="getStammName"
              label="Mein Stamm*"
              prepend-icon="mdi-account-group"
              :error-messages="stammErrors"
            >
              <template slot="append">
                <v-btn icon @click="onPickStammClick">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="info" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ tooltip.scoutOrganisation }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
            <pick-stamm-form ref="pickStamm" @sendIdToParent="tranferId" />
          </v-col>
          <v-col cols="12" sm="6">
            <v-text-field
              v-model="mobileNumber"
              label="Handynummer*"
              prepend-icon="mdi-cellphone"
              @change="updateData"
              :error-messages="mobileNumberErrors"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="info" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span>
                    {{ tooltip.mobileNumber }}
                  </span>
                </v-tooltip>
              </template>
            </v-text-field>
          </v-col>
          <v-col cols="12">
            <router-link to="/datenschutz" target="_blank">
              Link zur Datenschutzerklärung
            </router-link>
          </v-col>
          <v-col cols="12">
            <v-checkbox
              v-model="checkbox"
              label="Ich habe die Datenschutzerklärung gelesen und akzeptiert!"
              required
              :error-messages="checkboxErrors"
            ></v-checkbox>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>

    <v-card-actions>
      <v-container>
        <v-row>
          <v-col cols="12" sm="6" md="4">
            <v-btn color="success" @click="onSaveClicked">
              <v-icon left dark>mdi-check</v-icon>
              Änderungen speichern
            </v-btn>
          </v-col>
          <v-col cols="12" sm="6" md="4">
            <v-btn dark color="error" @click="onDeleteClicked">
              <v-icon left>mdi-delete</v-icon>
              Meine Daten löschen.
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-card-actions>
    <YesNoDialog ref="yesNoDialog" />
  </v-card>
</template>

<script>
import axios from 'axios';
import auth from '@/mixins/authMixin';
import { mapGetters } from 'vuex';
import { validationMixin } from 'vuelidate';
import { maxLength, minLength, required } from 'vuelidate/lib/validators';
import YesNoDialog from '@/components/modals/YesNoDialog.vue';
import PickStammForm from './PickStamm.vue';

export default {
  mixins: [validationMixin, auth],
  components: {
    PickStammForm,
    YesNoDialog,
  },
  validations: {
    scoutOrganisation: {
      required,
    },
    mobileNumber: {
      required,
      minLength: minLength(6),
      maxLength: maxLength(20),
    },
    scoutName: {
      required,
      maxLength: maxLength(20),
    },
    checkbox: {
      checked(val) {
        return val;
      },
    },
  },
  data() {
    return {
      API_URL: process.env.VUE_APP_API,
      loading: false,
      tooltip: {
        scoutName: 'Gib hier bitte deinen Namen oder deinen Fahrtennamen ein.',
        email:
          'Die E-Mail nutzen wir für die Kommunikation mit dem Tool und für Rückfragen.',
        mobileNumber:
          'Die Handynummer ist freiwillig und hilft dich zu kontaktieren (Für manche Fahrten ist sie Pflicht)',
        scoutOrganisation: 'Mit dem Stift kannst du deinen Stamm auswählen.',
      },
      user: null,
      scoutOrganisation: null,
      mobileNumber: '',
      scoutName: null,
      checkbox: false,
    };
  },
  computed: {
    ...mapGetters(['userinfo']),
    email() {
      return this.userinfo.email;
    },
    getStammName() {
      if (this.scoutOrganisation && this.scoutOrganisation.name) {
        return this.scoutOrganisation.name;
      }
      return 'Noch kein Stamm gewählt';
    },
    checkboxErrors() {
      const errors = [];
      if (!this.$v.checkbox.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.checkbox.checked &&
      errors.push('Du musst den Datenschutzbestimmungen zustimmen.');
      return errors;
    },
    mobileNumberErrors() {
      const errors = [];
      if (!this.$v.mobileNumber.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.mobileNumber.maxLength &&
      errors.push('Eine Handynummer hat maxtimal 20 Ziffern');
      // eslint-disable-next-line
      !this.$v.mobileNumber.minLength &&
      errors.push('Eine Handynummer hat mindestens 6 Ziffern.');
      // eslint-disable-next-line
      !this.$v.mobileNumber.required && errors.push('Dein Nummer ist erforderlich');
      return errors;
    },
    scoutNameErrors() {
      const errors = [];
      if (!this.$v.scoutName.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.scoutName.maxLength &&
      errors.push('Darf nicht mehr als 20 Zeichen haben');
      // eslint-disable-next-line
      !this.$v.scoutName.required && errors.push('Dein Name ist erforderlich');
      return errors;
    },
    stammErrors() {
      const errors = [];
      if (!this.$v.scoutOrganisation.$dirty) return errors;
      // eslint-disable-next-line
      !this.$v.scoutOrganisation.required &&
      errors.push('Wir brauchen deinen Stamm');
      return errors;
    },
  },
  methods: {
    updateData(type, data) {
      this[type] = data;
    },
    tranferId(newScoutOrganistation) {
      this.scoutOrganisation = newScoutOrganistation;
    },
    onPickStammClick() {
      this.$refs.pickStamm.show(this.scoutOrganisation);
    },
    onSaveClicked() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        return;
      }
      this.saveUserData();
    },
    async onDeleteClicked() {
      const text = 'Bist du sicher, dass du deinen Account beim Anmelde Tool löschen möchtest?'
        + '<p>Dies inkludiert:'
        + '<ul>'
        + '<li>Deine persöhnlichen Daten, wie deinen Fahrtennamen, deine Handynummer und deinen Stamm</li>'
        + '<li>Deine angebotenen Fahrten (sofern es keine anderen verantwortlichen Personen gibt)</li>'
        + '<li>Deine Registrierungen unabhängig ob sie bereits stattgefunden haben, oder erst noch stattfinden werden'
        + ' (sofern es keine anderen verantwortlichen Personen gibt)</li>'
        + '<li>Deine angebotenen Workshops</li>'
        + '</ul>'
        + '<p> Deine Daten beim DPV IDM bleiben allerdings weiterhin bestehen';
      const confirmBox = this.$refs.yesNoDialog.open(
        'Bestätige',
        text,
        'Löschen',
        'Abbrechen',
      );
      if (await confirmBox) {
        this.deleteUserData();
      }
    },
    getData() {
      this.loading = true;
      const path = `${this.API_URL}/auth/personal-data/`;
      axios.get(path)
        .then((res) => {
          this.scoutOrganisation = res.data.scoutOrganisation;
          this.mobileNumber = res.data.mobileNumber;
          this.scoutName = res.data.scoutName;
          this.checkbox = res.data.dsgvoConfirmed;
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Es gab einen Fehler beim runterladen deiner Daten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    saveUserData() {
      this.loading = true;
      const path = `${this.API_URL}/auth/personal-data/`;
      axios.post(path, {
        scoutOrganisation: this.scoutOrganisation.id,
        mobileNumber: this.mobileNumber,
        scoutName: this.scoutName,
        dsgvoConfirmed: this.checkbox,
      })
        .then(() => {
          this.$store.commit('setAccountIncomplete', false);
          this.$router.push({ name: 'eventOverview' });
          this.$root.globalSnackbar.show({
            message: 'Deine Daten wurden erfolgreich geändert.',
            color: 'success',
          });
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Es gab einen Fehler beim ändern deiner Daten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
    deleteUserData() {
      this.loading = true;
      const path = `${this.API_URL}/auth/personal-data/`;
      axios.delete(path)
        .then(() => {
          this.$root.globalSnackbar.show({
            message: 'Deine Daten wurden erfolgreich gelöscht.',
            color: 'success',
          });
          this.logout();
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Es gab einen Fehler beim löschen deiner Daten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  mounted() {
    this.getData();
  },
};
</script>
