<template>
  <v-container class="top-margin">
    <v-row class="center text-center justify-center">
      <v-card class="ma-2 pa-2 mx-auto">
        <div class="ma-3">
          <h2 class="py-4">Angaben gemäß § 5 TMG</h2>

          <p class="font-weight-medium">
            Pfadfinder-Bundesamt Köln e.V. <br />
            Deutscher Pfadfinderbund Mosaik <br />
            Robert-Perthel-Str. 79<br />
            50739 Köln <br />
          </p>

          <p>
            Der Deutsche Pfadfinderbund Mosaik hat die Rechtsform eines nicht
            eingetragenen Vereins.
          </p>

          <p>
            Rechtsträger aller Bundesstellen, Bundeseinrichtungen und
            Bundesunternehmungen ist: <br />
            <br />
            Pfadfinder-Bundesamt Köln e.V., <br />
            Robert-Perthel-Str. 79, <br />
            50739 Köln <br />
            VR 8654, Amtsgericht Köln<br />
          </p>
        </div>
      </v-card>
    </v-row>
    <v-row class="center text-center justify-center">
      <v-card class="ma-2 pa-2 mx-auto">
        <div class="ma-3">
          <h2 class="py-4">Kontakt:</h2>

          <p class="font-weight-medium">
            <a href="https://dpbm.de/impressum/">Kontakt zum Bundesamt hier </a>
            <br />
            <img
              alt="Email Adresse für Support Anfragen "
              class="mr-2"
              :src="require('@/assets/anmeldeToolMailAdresse.jpg')"
              height="50"
            />
            <br />
          </p>
        </div>
      </v-card>
      <v-card class="ma-4 pa-4 mx-auto">
        <div>
          <div class="ma-3">
            <h2 class="py-4">Haftung für Links</h2>

            <p class="font-weight-medium">
              Unser Angebot enthält Links zu externen Websites Dritter, auf
              deren Inhalte wir keinen Einfluss haben. Deshalb können wir für
              diese fremden Inhalte auch keine Gewähr übernehmen. Für die
              Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter
              oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten
              wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße
              überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der
              Verlinkung nicht erkennbar. Eine permanente inhaltliche Kontrolle
              der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer
              Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von
              Rechtsverletzungen werden wir derartige Links umgehend entfernen.
            </p>
          </div>
        </div>
      </v-card>
    </v-row>
    <v-row class="center text-center justify-center">
      <v-card class="ma-4 pa-4">
        <div>
          <div class="ma-3">
            <h2 class="py-4">Urheberrecht</h2>

            <p class="font-weight-medium">
              Die durch die Seitenbetreiber erstellten Inhalte und Werke auf
              diesen Seiten unterliegen dem deutschen Urheberrecht. Die
              Vervielfältigung, Bearbeitung, Verbreitung und jede Art der
              Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der
              schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
              Downloads und Kopien dieser Seite sind nur für den privaten, nicht
              kommerziellen Gebrauch gestattet. Soweit die Inhalte auf dieser
              Seite nicht vom Betreiber erstellt wurden, werden die
              Urheberrechte Dritter beachtet. Insbesondere werden Inhalte
              Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf eine
              Urheberrechtsverletzung aufmerksam werden, bitten wir um einen
              entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen
              werden wir derartige Inhalte umgehend entfernen
            </p>
            <a
              rel="license"
              href="https://creativecommons.org/licenses/by-nc/4.0/deed.de"
            >
              <img
                alt="Creative Commons Lizenzvertrag "
                style="border-width: 0"
                src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png"
              />
            </a>
            <br />
            Dieses Werk ist lizenziert unter einer
            <a
              rel="license"
              href="https://creativecommons.org/licenses/by-nc/4.0/deed.de"
            >
              Creative Commons Namensnennung-Nicht kommerziell 4.0 International
              Lizenz </a
            >.
          </div>
        </div>
      </v-card>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: [],

  data: () => ({
    dialog: false,
    data: [],
  }),
};
</script>
