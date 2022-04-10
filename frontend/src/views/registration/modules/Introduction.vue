<template>
  <GenericRegModul
    :key="`module-${moduleId}`"
    :loading="loading"
    :saving="saving"
    :position="position"
    :maxPos="maxPos"
    :currentMod="currentModule"
    @prevStep="prevStep"
    @nextStep="onNextStep"
    @ignore="onIngoredClicked"
    @saving="onSaving"
  >
    <template v-slot:header>
      <span class="text-left subtitle-1">
        <p>
          Hiermit melde ich meinen <b> {{ myStamm }} </b> aus dem Bund
          <b> {{ myBund }} </b> zu/r <b> {{ eventName }} </b> an.
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
import axios from 'axios';

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
    loading: true,
    saving: false,
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

          if (value && !value.length) {
            return true;
          }
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
    moduleId() {
      return this.currentModule.id;
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
    path() {
      return `event/registration/${this.currentRegistration.id}/attribute/`;
    },
  },
  mounted() {
    this.beforeTabShow();
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    onNextStep() {
      this.saving = true;
      const promises = [];
      this.moduleData.forEach((moduleItem) => {
        const getAtt = this.attributes.filter(
          (att) => att.templateId === moduleItem.attribute.id,
        );
        if (getAtt.length > 0) {
          promises.push(
            axios.put(
              `${process.env.VUE_APP_API}/${this.path}${getAtt[0].id}/`,
              {
                booleanField: this.data.checkboxes[moduleItem.id],
              },
            ),
          );
        } else {
          promises.push(
            axios.post(`${process.env.VUE_APP_API}/${this.path}`, {
              templateId: moduleItem.attribute.id,
              booleanField: this.data.checkboxes[moduleItem.id],
              resourcetype: moduleItem.attribute.resourcetype,
            }),
          );
        }
      });
      if (promises.length > 0) {
        Promise.all(promises).then(() => {
          this.nextStep();
        });
      } else {
        this.nextStep();
      }
    },
    getAttributeValue(item) {
      const value = this.attributes.filter(
        (att) => att.templateId === item.attribute.id,
      );
      if (value && value.length) {
        return value[0].booleanField;
      }
      return item.defaultValue;
    },
    setDefaults() {
      this.moduleData.forEach((item) => {
        this.data.checkboxes[item.id] = this.getAttributeValue(item);
      });
    },
    loadData() {
      this.saving = false;
      this.loading = true;
      Promise.all([
        this.getModule(this.currentModule.id, this.currentEvent.id),
        axios.get(`${process.env.VUE_APP_API}/${this.path}`),
        this.unConfirmRegistration(),
      ])
        .then((values) => {
          this.moduleData = values[0].data; //eslint-disable-line
          this.attributes = values[1].data; //eslint-disable-line
          this.loading = false;
          this.setDefaults();
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.loading = false;
        });
    },
    unConfirmRegistration() {
      return axios.put(
        `${process.env.VUE_APP_API}/event/registration/${this.currentRegistration.id}/`,
        {
          isConfirmed: false,
        },
      );
    },
  },
};
</script>
