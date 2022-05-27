<template>
  <v-container fluid class="pa-0">
    <v-row class="center text-center justify-center">
      <v-card class="pa-0" flat>
        <v-card-text class="pa-0">
          <v-container class="pa-0" fluid>
            <v-row class="center text-center justify-center  pa-0 mt-3">
              <v-col cols="8">
                <v-textarea
                  v-on:focus="$event.target.select()"
                  ref="responsiblePersonsInputField"
                  label="Planungsteam Emails"
                  outlined
                  :value="getResponsiblePersonsText"
                  readonly/>
              </v-col>
              <v-col cols="4">
                <v-row>
                  <v-btn @click="copy(getResponsiblePersonsText)">Kopieren</v-btn>
                </v-row>
                <v-row class="mt-6">
                  <v-btn @click="mailto(getResponsiblePersonsText)">
                    <v-icon>
                      mdi-email
                    </v-icon>
                    Mail an Planungsteam
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
            <v-row class="center text-center justify-center">
              <v-col cols="8">
                <v-textarea
                  v-on:focus="$event.target.select()"
                  ref="responsiblePersonsInputField"
                  label="Teilnehmer Emails"
                  outlined
                  :value="getRegistrationResponsiblePersonsText"
                  readonly/>
              </v-col>
              <v-col cols="4">
                <v-row>
                  <v-btn @click="copy(getRegistrationResponsiblePersonsText)">Kopieren</v-btn>
                </v-row>
                <v-row class="mt-6">
                  <v-btn @click="mailto(getRegistrationResponsiblePersonsText)">
                    <v-icon>
                      mdi-email
                    </v-icon>
                    Mail an Teilnehmer
                  </v-btn>
                </v-row>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-row>
    <v-row justify="center" class="overflow-y: auto">

    </v-row>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';

export default {
  mixins: [apiCallsMixin],
  data: () => ({
    responsiblePersons: [],
    registrationResponsiblePersons: [],
    loading: true,
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getResponsiblePersonsText() {
      const text = this.responsiblePersons.map((x) => x.email)
        .join(';');
      console.log(text);
      return text;
    },
    getRegistrationResponsiblePersonsText() {
      return this.registrationResponsiblePersons.map((x) => x.email)
        .join(';');
    },
  },
  methods: {
    onFilterSelected(values) {
      const params = new URLSearchParams();
      if (values) {
        values.forEach((value) => {
          params.append('booking-option', value);
        });
      }
      this.getData(this.eventId, params);
    },
    getData(eventId, param) {
      this.loading = true;

      Promise.all([
        this.getResponsiblePersons(eventId, param),
        this.getRegistrationsResponsiblePersons(eventId),
      ])
        .then((values) => {
          this.responsiblePersons = values[0].data; //eslint-disable-line
          this.registrationResponsiblePersons = values[1].data; //eslint-disable-line
          console.log(this.responsiblePersons);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    copy(text) {
      navigator.clipboard.writeText(text)
        .then((success) => {
          console.log(success);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    mailto(text) {
      window.location = `mailto:${text}`;
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
