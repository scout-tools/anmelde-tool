<template>
  <div>
    <section>
      <v-parallax
        :src="imageLink.main">
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
            color="primary"
            x-large
            @click="$router.push({ name: 'loginParticipants' })"
          >
            <v-icon left>mdi-calendar-plus</v-icon>
            Zu einem Lager Anmelden
          </v-btn>
        </v-layout>
      </v-parallax>
    </section>

    <section>
      <v-container>
        <v-layout column align-center justify-center class="white--text">
          <v-flex xs12 class="text-xs-center">
            <img height="200px" src="@/assets/logo_bdp_dpv_color.png"/>
          </v-flex>
        </v-layout>
      </v-container>
    </section>

    <section class="mb-12">
      <v-layout column wrap class="my-5" align-center>
        <v-flex xs12 sm4 class="my-3">
          <div class="text-xs-center">
            <h2 class="headline">
                Der Beste Weg um große Anmeldezahlen Übersichtlich zu gestalten.
            </h2>
            <span class="subheading">
                Kein E-Mail Krieg. Keine Missverständnisse. Zeit für das Wesentliche.
            </span>
          </div>
        </v-flex>
        <v-flex xs12 class="mb-12">
          <v-container grid-list-xl class="mb-12">
            <v-layout row wrap align-center>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">
                        <v-icon color="orange" x-large>mdi-baby-carriage</v-icon>
                        Einfach
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Schneller und Einfacher gab es keine Anmeldung für ein Pfadfinder_innen Lager.
                    Einloggen innerhalb von Sekunden ohne ein extra Passwort und du wirst durch
                    den Anmeldeprozess begleitet.
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline">
                        <v-icon color="green" x-large>mdi-beaker-check</v-icon>
                        Vollständig
                    </div>
                  </v-card-title>
                  <v-card-text>
                    Wer kennt es nicht? Du bekommst eine Anmeldung per E-Mail
                    und einige Informationen fehlen.
                    Es beginnt eine E-Mail Unterhaltung und das kostet wertvolle Zeit und nerven.
                    Eine Anmeldung über das Anmelde-Tool ist immer Vollständig.
                  </v-card-text>
                </v-card>
              </v-flex>
              <v-flex xs12 md4>
                <v-card class="elevation-0 transparent">
                  <v-card-title primary-title class="layout justify-center">
                    <div class="headline text-xs-center">
                        <v-icon color="red" x-large>mdi-shield-lock</v-icon>
                        Datenschutz</div>
                  </v-card-title>
                  <v-card-text>
                    Wir sorgen dafür, dass nur Personen die Daten
                    sehen, die sie auch (wirklich) brauchen.
                    Persönliche Daten werden gelöscht,
                    sobald sie nicht mehr gebraucht werden.
                  </v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </section>
  </div>
</template>

<script>
export default {
  data: () => ({
    title: 'Endorfine',
    imageLink: {
      sub_main:
        'https://wiki.hratuga.de/files/public-docs/2018-05-Fu%CC%88hrungstippel-63-klein.jpg',
      main:
        'https://wiki.hratuga.de/files/public-docs/Italien-Robert-9_klein.jpg',
      logo:
        'https://wiki.hratuga.de/files/public-docs/logo_bdp_dpv.png',
      social_cover:
        'https://firebasestorage.googleapis.com/v0/b/endorfinevue.appspot.com/o/assets%2Fo-NIGHTCLUB-facebook.jpg?alt=media&token=cefc5c4c-9714-41da-9c22-f63caf5e89a4',
    },
    email: '',
    subscribed: false,
  }),
};
</script>

<style>
</style>
