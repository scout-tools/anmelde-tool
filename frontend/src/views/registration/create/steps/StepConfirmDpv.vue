<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row class="mt-2">
        <span class="text-left subtitle-1">
          <p><b>Zusammenfassung</b></p>
            <p>Hier folgt nun deine Datenübersicht.
              Bitte vergewissere Dich, dass alles richtig ist und klicke anschließend auf Absenden:
            </p>
            <p>
              Du
              <b>{{currentRegistrationSummary[0].responsiblePersons[0].userextended_ScoutName}}</b>
              hast
              <b>{{currentRegistrationSummary[0].scoutOrganisation}}</b>
              für das BdP-DPV stadt&spiel für das Wochenende vom 17.-19.September 2021 mit insgesamt
              <b>{{currentRegistrationSummary[0].totalParticipants}}</b>
              Teilnehmende angemeldet.
            </p>

        </span>
        <v-expansion-panels accordion>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Verantwortliche Person:
              <b>{{currentRegistrationSummary[0].responsiblePersons[0].userextended_ScoutName}}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              E-Mail-Adresse:
              <b>{{currentRegistrationSummary[0].responsiblePersons[0].username}}</b><br>
              Telefon/Handy (freiwillig):
              <b>{{currentRegistrationSummary[0].responsiblePersons[0].userextended_MobileNumber}}
              </b><br>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Teilnehmende insgesamt: <b>{{currentRegistrationSummary[0].totalParticipants}}</b>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Das sind die Daten deines Stammes<br>
              <li v-for="item in currentRegistrationSummary[0].groupParticipants"
                  :key="item.participantRoleId">
                {{ item.participantRoleId_Name }}:
                <b>{{ item.participantRoleId }}</b>
              </li>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Eigene Schlafstätte {Heim/Lagerplatz/beides}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              Heim/Lagerplatz: {ja/nein}
(wenn ja)
=>Zu Daten des Heims, sonst
Daten des Heims:
Adresse: {Straße, Hausnummer, Postleitzahl, Stadt}
Schlafplatzanzahl:
-Haus (ohne Corona/mit Corona): {Zahl Im Haus/Zahl Im Haus Corona}
-Zeltplatz (ohne Corona/mit Corona): {Zahl Zeltplatz/Zahl Zeltplatz mit Corona}
Kosten:
-Pro Person: {Zahl der Kosten pro Person}
-Fixkosten: {Zahl von Fixkosten}
Die Kontaktperson für Haus/Lagerplatz {Name der Kontaktperson} ist wie folgt zu erreichen:
              {E-mail und/oder Telefonnummer}
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Da wollen wir hin {weg/hier}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
Dort geht es für deinen Stamm hin:
Hier gibt es folgende Möglichkeiten:
{Wir wollen bei uns im Heim bleiben und besucht werden/Wir wollen einen anderen Stamm besuchen und
              stellen unser Heim zur Verfügung/wir bleiben da, fahren aber auch gerne weg}
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Zusätzliche Schlafstätte {Name}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
Du hast ein zusätzliches Heim eingetragen mit folgenden Daten:
Name: {Name der Schlafstätte}
Kontakt: {Name Kontaktperson} ist zu erreichen unter {E-Mail und/oder Telefonnummer}
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              Paket {Vor-Nachnamen}
            </v-expansion-panel-header>
            <v-expansion-panel-content>
Für ein Paket an deinen Stamm hast Du folgende Adresse angegeben:
Name und Adresse: {Vorname, Nachname, Straße und Hausnummer,
              Postleitzahl und Ort, evtl. Adresszusatz}
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-row>
      <v-divider class="text-left my-2" />
      <v-row>
        <v-checkbox
          v-model="data.checkbox1"
          :label="`Ich habe meine Daten überprüft und melde meinen Stamm verbindlich zur Fahrt an.`"
        >
        </v-checkbox>
      </v-row>

      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required } from 'vuelidate/lib/validators';
import axios from 'axios';
import { mapGetters } from 'vuex';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepNameDescription',
  displayName: 'Zusammenfassung und Bestätigung',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    data: {
      checkbox1: false,
    },
  }),
  validations: {
    data: {
      checkbox1: {
        required,
        checked: (value) => value === true,
      },
    },
  },
  computed: {
    ...mapGetters(['currentRegistrationSummary']),
    id() {
      return this.$route.params.id;
    },
  },
  methods: {
    async getRegistrationSummaryData() {
      const path = `${process.env.VUE_APP_API}basic/registration/${this.id}/summary/`;
      axios
        .get(path)
        .then((res) => {
          this.$store.commit('setCurrentRegistrationSummary', res.data);
        })
        .catch(() => {
          console.log('Fehler');
        });
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
      this.valid = !this.$v.$error;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
    beforeTabShow() {
      this.getRegistrationSummaryData();
    },
  },
};
</script>
