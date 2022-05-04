<template>
  <v-form ref="formEventContact" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Du hast dich für eine Rechtemanagement mit Email Adressen entschieden!
            Jeder der Zugriff auf die Interna deines Events bekommen soll, muss hier mit seiner
            Email Adresse aufgeführt werden.
          <br/>
          <i>(Jede geschriebene E-Mail-Adresse muss mit Enter bestätigt werden!)</i>
        </span>
      </v-row>
      <v-row>
        <div v-for="(field, i) in fields" :key="i">
          <BaseField
            :field="field"
            v-model="data[field.techName]"
            :valdiationObj="$v"
          />
        </div>
      </v-row>

      <v-divider class="my-2"/>

      <prev-next-button
        :valid="valid"
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submitStep="submitStep"
        @ignore="onIngoredClicked"
        @update="updateData"
      />
    </v-container>
  </v-form>
</template>

<script>
import { required, email } from 'vuelidate/lib/validators';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepEventAuthenticationInternal',
  header: 'Intere Auth-Verwaltung',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    PrevNextButton,
    BaseField,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    modulePath: '/event/event/',
    data: {},
    fields: [
      {
        name: 'Kontaktdaten',
        techName: 'responsiblePersons',
        tooltip: 'Wähle die Keycloak Gruppe aus in der das Planungsteam ist. Falls die Gruppe fehlt bitte dem DPV bescheid geben.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'simpleCombo',
        default: '',
        cols: 12,
      },
    ],
  }),
  validations: {
    data: {
      responsiblePersons: {
        $each: {
          required,
          email,
        },
      },
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getServiceById('event/event', this.id).then((response) => {
        this.data.responsiblePersons = response.data.responsiblePersons;
        this.$forceUpdate();
      });
    },
  },
  // created() {
  //   this.loadData();
  // },
};
</script>
