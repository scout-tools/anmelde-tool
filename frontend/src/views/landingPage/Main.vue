<template>
  <div>
    <section>
      <v-parallax :src="image1Path">
        <v-layout column align-center justify-center class="white--text">
          <h1
            class="white--text mb-2 display-1"
            style="font-weight: 900; text-shadow: 3px 2px #000000"
          >
            Das Pfadfinder_innen Anmelde-Tool
          </h1>
          <div
            class="white--text subheading mb-3"
            style="font-weight: 900; text-shadow: 2px 2px #000000"
          >
            Einfach. Schnell. Übersichtlich.
          </div>
          <v-btn
            class="mt-10"
            color="success"
            x-large
            @click="onLoginClicked"
            v-if="!isAuth"
          >
            <v-icon left>mdi-rocket-launch</v-icon>
            Los geht's
          </v-btn>
          <v-btn
            class="mt-10"
            color="success"
            x-large
            @click="$router.push({ name: 'eventOverview' })"
            v-if="isAuth"
          >
            <v-icon left>mdi-rocket-launch</v-icon>
            Zu den Anmeldungen
          </v-btn>
        </v-layout>
      </v-parallax>
    </section>

    <section>
      <v-container>
        <v-layout column align-center justify-center class="white--text">
          <v-flex xs12 class="text-xs-center">
            <img height="200px" :src="getLogoPath" alt="f" />
          </v-flex>
        </v-layout>
      </v-container>
    </section>

    <section class="mb-12">
      <v-layout column wrap class="my-5" align-center>
        <v-flex xs12 sm4 class="my-3">
          <div class="text-xs-center">
            <h2 class="headline">
              Der beste Weg, um große Anmeldezahlen übersichtlich zu gestalten.
            </h2>
            <span class="subheading">
              Keine E-Mail Missverständnisse. Zeit für das
              Wesentliche.
            </span>
          </div>
        </v-flex>
        <v-flex xs12 class="mb-12">
          <v-container grid-list-xl class="mb-12">
            <v-row>
              <v-col cols="4">
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">
                      <v-icon color="orange" x-large>mdi-baby-carriage</v-icon>
                      Einfach
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Schneller und einfacher war eine Anmeldung für ein Fahrt
                    noch nie. Die Anmeldung deiner Teilnehmende klappt innerhalb
                    von Minuten. Kein extra Passwort. Der Anmeldeprozess ist gut
                    erklärt, sodass keine Fragen offen bleiben. Falls sich eine
                    Änderung ergeben hat, können die Daten bis zum
                    Anmeldeschluss einfach noch schnell angepasst werden.
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="4">
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline">
                      <v-icon color="green" x-large>mdi-beaker-check</v-icon>
                      Vollständig
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Wer kennt es nicht? Du bekommst eine Anmeldung per E-Mail
                    und einige Informationen fehlen. Es beginnt eine E-Mail
                    Unterhaltung und das kostet wertvolle Zeit und Nerven. Eine
                    Anmeldung über das Anmelde-Tool ist immer vollständig.
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="4">
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">
                      <v-icon color="red" x-large>mdi-shield-lock</v-icon>
                      Datenschutz
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Wir sorgen dafür, dass nur Personen die Daten sehen, die sie
                    auch (wirklich) brauchen. Persönliche Daten werden gelöscht,
                    sobald sie nicht mehr gebraucht werden.
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-flex>
      </v-layout>
    </section>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import basicInfoMixin from '@/mixins/basicInfoMixin';
import authMixin from '@/mixins/authMixin';

export default {
  mixins: [basicInfoMixin, authMixin],
  data: () => ({
    title: 'Endorfine',
    email: '',
    subscribed: false,
  }),
  computed: {
    ...mapGetters(['theme']),
    logoPath() {
      if (process.env.VUE_APP_ENV === 'DEV') {
        return require(`./../../assets/${this.theme}/logo-dev.png`); // eslint-disable-line
      }
      return require(`./../../assets/${this.theme}/logo.png`); // eslint-disable-line
    },
    image1Path() {
      return require(`./../../assets/${this.theme}/image1.jpg`); // eslint-disable-line
    },
  },
  methods: {
    onLoginClicked() {
      this.$keycloak.login();
    },
  },
};
</script>
