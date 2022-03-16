<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :isloading="isLoadingRead"
    :position="position"
    :maxPos="maxPos"
    @prevStep="prevStep"
    @nextStep="nextStep"
    @ignore="onIngoredClicked"
  >
    <template v-slot:header>
      <span class="text-left subtitle-1">
        <p>
          Hiermit melde ich mich vom<b> {{ myStamm }} </b> aus dem Bund
          <b> {{ myBund }} </b> zur <b> {{ eventName }} </b> an.
          <br />
          <br />
          Bevor deine Anmeldung verbindlich wird, musst du sie im letzten
          Schritt ausdrücklich bestätigen. Du kannst deinen Anmeldevorgang zu
          jedem Zeitpunkt unterbrechen und später fortsetzen. Die Daten kannst
          du bis zum Anmeldeschluss ({{ registrationDeadlineFormat }}) jederzeit
          anpassen und ergänzen. <br />
          <br />
          Die folgenden Daten sind nur für das Planungsteam und die
          Administrator_innen sichtbar. <br />
          <span v-if="cloudLink">Alle Dokumente findest du hier:</span>
          <a v-if="cloudLink" target="_blank" :href="cloudLink">
            Link zur Cloud
          </a>
        </p>
      </span>
    </template>

    <template v-slot:main>
      <v-row v-for="checkbox in moduleData" :key="checkbox.id">
        <v-checkbox
          v-model="data.checkboxes[checkbox.id]"
          :label="checkbox.text ? checkbox.text : ''"
          :error-messages="errorMessage('checkboxes', $v)"
        >
        </v-checkbox>
      </v-row>
    </template>
  </GenericRegModul>
</template>

<script>
import { mapGetters } from 'vuex';
import moment from 'moment';

import apiCallsMixin from '@/mixins/apiCallsMixin';
import stepMixin from '@/mixins/stepMixin';
import { required } from 'vuelidate/lib/validators';
import GenericRegModul from '@/views/registration/components/GenericRegModul.vue';

export default {
  name: 'StepConsent',
  displayName: 'Einverständnis',
  props: [
    'position',
    'maxPos',
    'currentEvent',
    'currentRegistration',
    'currentModule',
    'personalData',
  ],
  components: {
    GenericRegModul,
  },
  mixins: [apiCallsMixin, stepMixin],
  data: () => ({
    valid: true,
    moduleData: [],
    isloading: false,
    data: {
      checkboxes: [],
    },
  }),
  validations: {
    data: {
      checkboxes: {
        required,
        allChecked: (value) => {
          const values = Object.values(value);
          console.log(values && values.every((item) => item));
          return values && values.every((item) => item);
        },
      },
    },
  },
  computed: {
    ...mapGetters(['userinfo']),
    registrationDeadlineFormat() {
      return moment(this.currentEvent.registrationDeadline)
        .lang('de')
        .format('ll');
    },
    isLoadingRead: {
      // getter
      get() {
        return !!this.isloading;
      },
      set() {},
    },
    moduleId() {
      return this.currentModule.module.id;
    },
    myStamm() {
      return this.userinfo.stamm;
    },
    myBund() {
      return this.userinfo.bund;
    },
    eventName() {
      return this.currentEvent.name;
    },
    cloudLink() {
      return this.currentEvent.cloudLink;
    },
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    setDefaults() {
      this.moduleData.forEach((data) => {
        this.data.checkboxes[data.id] = false;
      });
    },
    loadData() {
      this.isLoading = true;
      Promise.all([this.getModule(this.moduleId)])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.isLoading = false;
          this.setDefaults();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
  },
};
</script>
