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
    <v-card outlined class="ma-3 pa-3" :loading="sendMailLoading" v-if="isTeam">
      <v-card-title>
        Email an Teilnehmer verschicken
      </v-card-title>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="3">
          <v-checkbox
              v-model="sendMail.sendConfirmed"
              label="Bestätigte"
              hide-details/>
        </v-col>
        <v-col cols="3">
          <v-checkbox
              v-model="sendMail.sendUnconfirmed"
              label="Unbestätigte"
              hide-details/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-text-field
              label="Betreff"
              outlined
              v-model="sendMail.subject"/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-text-field
              label="Kopfzeile"
              outlined
              v-model="sendMail.header"/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="12">
          <ckeditor
              :editor="ckeditor.editor"
              v-model="sendMail.body"
              :config="ckeditor.editorConfig"/>
        </v-col>
      </v-row>
      <v-row class="center text-center justify-center pa-0">
        <v-col cols="6">
          <v-btn @click="sendCustomMail" :disabled="sendMailDisabled">
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
import axios from 'axios';
import { mapGetters } from 'vuex';
// import BookingFilter from '@/components/common/BookingFilter.vue';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import '@ckeditor/ckeditor5-build-classic/build/translations/de';

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
    sendMailLoading: false,
    sendMail: {
      subject: 'Es gibt Neuigkeiten',
      body: 'Hallo,\n',
      sendConfirmed: true,
      sendUnconfirmed: true,
      header: 'Es gibt Neuigkeiten',
    },
    sendMailDisabled: false,
    ckeditor: {
      editor: ClassicEditor,
      editorData: '',
      editorConfig: {
        language: 'de',
      },
    },
  }),
  computed: {
    ...mapGetters(['userinfo']),
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
    isTeam() {
      if (this.userinfo && this.userinfo.roles && this.userinfo.roles.length > 0) {
        return this.userinfo.roles.includes('anmelde_tool_team');
      }
      return 0;
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
    sendCustomMail() {
      this.sendMailDisabled = true;
      this.sendMailLoading = true;
      const path = `${process.env.VUE_APP_API}/event/event/${this.eventId}/email/custom-mail/`;
      axios.post(path, {
        body: this.sendMail.body,
        subject: this.sendMail.subject,
        header: this.sendMail.header,
        sendConfirmed: this.sendMail.sendConfirmed,
        sendUncofirmed: this.sendMail.sendUnconfirmed,
      })
        .then(() => {
          this.$root.globalSnackbar.show({
            message: 'Email erfolgreich verschickt.',
            color: 'success',
          });
        })
        .catch((error) => {
          console.log(error);
          this.$root.globalSnackbar.show({
            message: 'Es gab einen Fehler beim verschicken der Mail, bitte probiere es später noch einmal.',
            color: 'error',
          });
        })
        .finally(() => {
          this.sendMailLoading = false;
            setTimeout(() => this.sendMailDisabled = false, 1000);// eslint-disable-line
        });
    },
  },
  created() {
    this.getData(this.eventId);
  },
};
</script>
