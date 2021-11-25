<template>
  <v-container class="top-margin">
    <v-row class="center text-center justify-center">
      <p>
        Bei Fragen aller Art könnt ihr euch bei uns melden:
        <br/>
        <img
          alt="Email Adresse für Support Anfragen"
          class="mr-2"
          :src="require('@/assets/anmeldeToolMailAdresse.jpg')"
          height="50"
        /></p
      ></v-row>
    <v-row class="center text-center justify-center">
      <v-divider/>
      <v-expansion-panels>
        <v-expansion-panel v-for="(faq, i) in faqs" :key="i">
          <v-expansion-panel-header>
            <span class="title ma-3"> {{ faq.question }}</span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <p class="text-left subtitle-1 pa-3" v-html="faq.answer"></p>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    faqs: [
      {
        question: 'Zusammenfassung',
        answer:
          'Unser Ziel ist es so wenig persönliche Daten wie möglich zu erfassen, zu verarbeiten und natürlich auch zu speichern. Wir betreiben Datenvermeidung und setzen technisch hohe Maßstäbe an.',
      },
      {
        question: 'Datenspeicherung für nicht „eingeloggten User“',
        answer:
          'Wir speichern keine Daten von nicht eingeloggten Besuchern dauerhaft. Wir nutzen auch keinerlei Cookies, um deinen digitalen Fingerabdruck zu speichern. Unser Server Anbieter hat ebenfalls nicht die Möglichkeit deine Daten zu verarbeiten. <br> <br>' + // eslint-disable-line
          'Aus technischen Gründen verarbeiten unsere Server deine persönlichen Daten für die Dauer des Besuchs auf unserer Seite. Wir verarbeiten deine IP-Adresse, damit wir in der Lage sind deine Anfrage zum Seitenaufruf zu beantworten. Alle Logdateien werden anonymisiert gespeichert und sich in keine weise nutzbar um dich als Person zu identifizieren.',
      },
      {
        question: 'Datenspeicherung für „eingeloggten User“',
        answer:
          'Um sich einzuloggen müssen wir deine persönlichen Daten dauerhaft speichern. Es dient dem Zweck des Anmeldetools, dass wir deine Anmeldung dir zuordnen können. Dazu speichern wir:' + // eslint-disable-line
          '<ul><li>Deine E-Mail-Adresse</li><li>Deinen Pfadfindernamen</li><li>Ggf. deine Telefonnummer (die Fahrtenleitung entscheidet darüber, ob das Feld verpflichtend ist)</li></ul>',
      },
      {
        question: 'Empfänger / Weitergabe von Daten (an Dritte )',
        answer:
          'Deine Persönlichen Daten sind grundsätzlich für zwei Personengruppen sichtbar: <br> <br>' + // eslint-disable-line
          '<b>Fahrtenleitungen:</b> Jede Fahrtenleitung hat Zugriff auf deinen Namen, deine E-Mail-Adresse und deine Telefonnummer nachdem zu dich für die Fahrt ausdrücklich als Verantwortlicher eingetragen hast.<br> <br>' + // eslint-disable-line
          '<b>Administratoren vom Anmelde-Tool:</b> Um den ordnungsgemäßen Betrieb des Anmelde-Tools zu gewährleisten haben ausdrücklich vom Pfadfinder-Bundesamt Köln e.V. ausgewählte Personen Zugriff auf die Daten. Diese Personen können wechseln und werden protokolliert. <br> <br>' + // eslint-disable-line
          '<b>Dritte:</b> Darüberhinaus erfolg keine Datenweitergabe an Dritte .',
      },
      {
        question: 'Verschlüsselung',
        answer:
          'Jede Kommunikation mit dem Anmelde-tool läuft über eine im Internet übliche SSL Verschlüsselung.',
      },
      {
        question: 'Deine Rechte (z.B. Auskunft / Löschung)',
        answer:
          'Recht auf Auskunft (Artikel 15 der Datenschutz-Grundverordnung)' + // eslint-disable-line
          '<ul><li>Recht auf Berichtigung (Artikel 16 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Löschung ("Recht auf Vergessenwerden") (Artikel 17 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Einschränkung der Verarbeitung (Artikel 18 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Datenübertragbarkeit (Artikel 20 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Widerspruch (Artikel 21 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Widerruf von Einwilligungen (Artikel 7 Absatz 3 der Datenschutz-Grundverordnung)</li>' + // eslint-disable-line
          '<li>Recht auf Beschwerde bei der Aufsichtsbehörde (Artikel 57 Absatz 1 Buchstabe f der Datenschutz-Grundverordnung)</li></ul><br>' + // eslint-disable-line
          'Wenn du eine dieser Rechte wahrnehmen willst kannst du uns jederzeit anschreiben. Wir werden dir dann individuell weiterhelfen. <br><br>' + // eslint-disable-line
          'Bei einer Auskunftsanfrage, die nicht schriftlich erfolgt und die nicht anderweitig sicher verifiziert werden kann, musst du damit rechnen, dass wir Nachfragen stellen. Wir müssen sicherstellen, dass du die Person bist, für die du Dich ausgibst.',
      },
      {
        question: 'Datenverarbeitung außerhalb der Europäischen Union',
        answer:
          'Wir nutzen für die Datenverarbeitung Server von „Amazon Web Services Inc.“ alle persönlichen Daten sind in den drei Rechenzentren eu-central-1 a,b,c also in Frankfurt gespeichert. Wir nutzen für die Speicherung und der Verarbeitung deiner persönlichen Daten keine Server außerhalb Deutschlands.',
      },
      {
        question: 'EU-US Privacy Shield',
        answer:
          'Amazon ist ein US-Amerikanisches Unternehmen und seitdem der Europäische Gerichtshof das Privacy-Shield für ungültig erklärt hat ist die Rechtslage undurchsichtiger geworden. <br> <br>' + // eslint-disable-line
          'Amazon beschreibt die Rechtslage auf der Internetseite wie folgt: <br><br>' + // eslint-disable-line
          '<i>AWS bietet Kunden eine Reihe von Möglichkeiten zur Einhaltung der europäischen Datenschutzgesetze. Beispielsweise können sich Kunden auf den AWS GDPR-Datenverarbeitungszusatz (Data Processing Addendum) verlassen, der die von der Artikel-29-Datenschutzgruppe genehmigten Standardvertragsklauseln enthält (Data Processing Addendum). Der Zusatz zur Datenverarbeitung steht allen AWS-Kunden zur Verfügung, die Daten aus der EU in eine der AWS-Regionen in der ganzen Welt übertragen, ob nun in die USA oder nicht. Der Zusatz zur Datenverarbeitung bietet Kunden die Sicherheit, dass AWS die Daten der Kunden nach den gleichen hohen Sicherheits- und Datenschutzstandards behandelt, die sie auch in der EU erhalten würden.</i><br>' + // eslint-disable-line
          'Weitere Informationen findest du <a href="https://aws.amazon.com/de/compliance/eu-us-privacy-shield-faq/">hier</a>',
      },
      {
        question: 'Cookies',
        answer:
          'Wir speichern keine deiner Cookies, mit denen wir eine Person identifizieren können. <br> Wir tracken kein Nutzerverhalten. <br>Wir speichern keine Daten für eine Webeanalyse. <br>Wir nutzen keinerlei Marketing-Tools. <br><br>Cookies werden nur für die technisch saubere Nutzung der App verwendet.',
      },
      {
        question: 'Verantwortlich für die Datenverarbeitung',
        answer:
          'Pfadfinder-Bundesamt Köln e.V.<br>' + // eslint-disable-line
          'Deutscher Pfadfinderbund Mosaik,<br>' + // eslint-disable-line
          'Robert-Perthel-Str. 79<br>' + // eslint-disable-line
          '50739 Köln<br>' + // eslint-disable-line
          'Telefon: 02 21 – 52 40 18<br>',
      },
      {
        question: 'Datenschutzbeauftragter',
        answer:
          'Wir nehmen das Thema Datenschutz besonders ernst, weil es einer der Hauptgründe ist warum das Tool entwickelt wurde. <br>Wir sind gesetzlich nicht verpflichtet, einen Datenschutzbeauftragten zu benennen und haben auch keinen Datenschutzbeauftragten benannt.',
      },
      {
        question: 'Änderung dieser Datenschutzhinweise',
        answer:
          'Wir überarbeiten diese Datenschutzhinweise bei Änderungen an dieser Internetseite oder bei sonstigen Anlässen, die dies erforderlich machen. Die jeweils aktuelle Fassung findest du stets auf dieser Internetseite.',
      },
      {
        question: 'Sonstige Fragen zum Datenschutz',
        answer:
          'Wenn du Fragen zum Datenschutz hast, kannst du Dich gerne uns mich wenden. ', // eslint-disable-line
      },
    ],
  }),
};
</script>
