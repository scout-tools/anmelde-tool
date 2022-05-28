<template>
  <v-container fluid class="pa-0">
    <v-card outlined class="ma-3 pa-3" :loading="loading">
      <v-card-title>
        Emails des Planungsteams
      </v-card-title>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-checkbox
            v-model="filterresponsiblePersons"
            label="Nur Lagerleitung"
            hide-details
            @change="onFilterSelected"/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="12">
          <v-textarea
            v-on:focus="$event.target.select()"
            ref="responsiblePersonsInputField"
            label="Planungsteam Emails"
            outlined
            :value="getResponsiblePersonsText"
            readonly/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-btn @click="copy(getResponsiblePersonsText)">Kopieren</v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn @click="mailto(getResponsiblePersonsText)">
            <v-icon>
              mdi-email
            </v-icon>
            Mail an Planungsteam
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-card outlined class="ma-3 pa-3" :loading="loading">
      <v-card-title>
        Emails der verantwortlichen Teilnehmer
      </v-card-title>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="3">
          <v-checkbox
            v-model="filterRegistrationResponiblePersons.confirmed"
            label="Bestätigte"
            hide-details
            @change="onFilterSelected"/>
        </v-col>
        <v-col cols="3">
          <v-checkbox
            v-model="filterRegistrationResponiblePersons.unconfirmed"
            label="Unbestätigte"
            hide-details
            @change="onFilterSelected"/>
        </v-col>
<!--        <v-col cols="3">-->
<!--          <v-tooltip bottom>-->
<!--            <template v-slot:activator="{ on, attrs }">-->
<!--              <v-checkbox-->
<!--                v-model="filterRegistrationResponiblePersons.allParticipants"-->
<!--                label="Alle Teilnehmer"-->
<!--                hide-details-->
<!--                @change="onFilterSelected"-->
<!--                v-bind="attrs"-->
<!--                v-on="on"/>-->
<!--            </template>-->
<!--            <span>Füge alle Teilnehmer hinzu, deren Email Adresse angebeben wurde.</span>-->
<!--          </v-tooltip>-->
<!--        </v-col>-->
<!--        <v-col cols="3">-->
<!--          <v-tooltip bottom>-->
<!--            <template v-slot:activator="{ on, attrs }">-->
<!--              <BookingFilter-->
<!--                :loading="loading"-->
<!--                :bookingOptionList="bookingOptionList"-->
<!--                @onFilterSelected="onFilterSelected"-->
<!--                v-model="filterRegistrationResponiblePersons.selectedBookingOption"-->
<!--                v-bind="attrs"-->
<!--                v-on="on"-->
<!--              />-->
<!--            </template>-->
<!--            <span>Filter die Verantwortlichen,-->
<!--              wo mindestens ein Teilnehmer die selektierte Option gebucht hat.</span>-->
<!--          </v-tooltip>-->
<!--        </v-col>-->
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="12">
          <v-textarea
            v-on:focus="$event.target.select()"
            ref="responsiblePersonsInputField"
            label="Teilnehmer Emails"
            outlined
            :value="getRegistrationResponsiblePersonsText"
            readonly/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-btn @click="copy(getRegistrationResponsiblePersonsText)">Kopieren</v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn @click="mailto(getRegistrationResponsiblePersonsText)">
            <v-icon>
              mdi-email
            </v-icon>
            Mail an Teilnehmer
          </v-btn>
        </v-col>
      </v-row>
    </v-card>
    <v-snackbar
      v-model="showSnackbar"
      timeout="2000"
      :color="snackbarColor"
      rounded
      top>
      <div class="center text-center justify-center">
        {{ snackbarText }}
      </div>
    </v-snackbar>
  </v-container>
</template>

<script>
import apiCallsMixin from '@/mixins/apiCallsMixin';
// import BookingFilter from '@/components/common/BookingFilter.vue';

export default {
  mixins: [apiCallsMixin],
  // components: {
  //   BookingFilter,
  // },
  data: () => ({
    responsiblePersons: [],
    registrationResponsiblePersons: [],
    filterresponsiblePersons: false,
    filterRegistrationResponiblePersons: {
      confirmed: true,
      unconfirmed: true,
      selectedBookingOption: [],
      allParticipants: false,
    },
    bookingOptionList: [],
    loading: true,
    showSnackbar: false,
    snackbarText: '',
    snackbarColor: 'green',
  }),
  computed: {
    eventId() {
      return this.$route.params.id;
    },
    getResponsiblePersonsText() {
      return this.responsiblePersons.map((x) => x.email)
        .join(';');
    },
    getRegistrationResponsiblePersonsText() {
      return this.registrationResponsiblePersons.map((x) => x.email)
        .join(';');
    },
  },
  methods: {
    onFilterSelected() {
      const paramsResponsiblePersons = new URLSearchParams();
      if (this.filterresponsiblePersons) {
        paramsResponsiblePersons.append('only-admins', this.filterresponsiblePersons);
      }
      const paramsRegistrationResponsiblePersons = new URLSearchParams();
      if (this.filterRegistrationResponiblePersons) {
        paramsRegistrationResponsiblePersons.append('confirmed', this.filterRegistrationResponiblePersons.confirmed);
        paramsRegistrationResponsiblePersons.append('unconfirmed', this.filterRegistrationResponiblePersons.unconfirmed);
        // paramsResponsiblePersons.append('all-participants',
        // this.filterRegistrationResponiblePersons.allParticipants);
        // this.filterRegistrationResponiblePersons.selectedBookingOption.forEach((value) => {
        //   paramsResponsiblePersons.append('booking-option', value);
        // });
      }
      this.getData(this.eventId, paramsResponsiblePersons, paramsRegistrationResponsiblePersons);
    },
    getData(eventId, paramsResponsiblePersons, paramsRegistrationResponsible) {
      this.loading = true;

      Promise.all([
        this.getResponsiblePersons(eventId, paramsResponsiblePersons),
        this.getRegistrationsResponsiblePersons(eventId, paramsRegistrationResponsible),
        this.getBookingOptions(eventId),
      ])
        .then((values) => {
          this.responsiblePersons = values[0].data; //eslint-disable-line
          this.registrationResponsiblePersons = values[1].data; //eslint-disable-line
          this.bookingOptionList = values[2].data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    copy(text) {
      navigator.clipboard.writeText(text)
        .then(() => {
          this.showSnackbar = true;
          this.snackbarText = 'Kopiert';
          this.snackbarColor = 'green';
        })
        .catch((err) => {
          this.showSnackbar = true;
          this.snackbarText = err;
          this.snackbarColor = 'red';
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
