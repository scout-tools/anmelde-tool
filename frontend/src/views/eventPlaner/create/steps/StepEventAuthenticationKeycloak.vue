<template>
  <v-form ref="StepEventAuthenticationKeycloak" v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
            Du hast dich für eine Rechtemanagement mit dem DPV IDM entschieden, cool!
            So kann jeder der z.b. Zugriff im Wiki oder in der Cloud auf dein Event hat, auch hier
            Einsicht in deine Aktion bekommen.
          <br/>
           Wähle dazu einfach aus der Liste die entsprechende IDM Gruppe aus.
          <br/>
        </span>
      </v-row>
      <div v-for="(field, i) in fields" :key="i">
        <BaseField
          :field="field"
          v-model="data[field.techName]"
          :valdiationObj="$v"
        />
      </div>
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
import { required } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepEventAuthenticationKeycloak',
  header: 'DPV IDM',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  components: {
    PrevNextButton,
    BaseField,
  },
  mixins: [stepMixin, apiCallsMixin, serviceMixin],
  data: () => ({
    valid: true,
    data: {},
    modulePath: '/event/event/',
    fields: [
      {
        name: 'Planungsteamgruppe auswählen',
        techName: 'keycloakPath',
        tooltip: 'Wähle die Keycloak Gruppe aus in der das Planungsteam ist. Falls die Gruppe fehlt bitte dem DPV bescheid geben.',
        icon: 'mdi-account-circle',
        lookupPath: '/auth/groups/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
      {
        name: 'Lagerleitungsgruppe auswählen',
        techName: 'keycloakAdminPath',
        tooltip: 'Wähle die Keycloak Gruppe aus in die Lagerleitung ist. Falls die Gruppe fehlt bitte dem DPV bescheid geben.',
        icon: 'mdi-account-circle',
        lookupPath: '/auth/groups/',
        lookupListDisplay: ['name'],
        mandatory: true,
        fieldType: 'refDropdown',
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      keycloakPath: {
        required,
      },
      keycloakAdminPath: {
        required,
      },
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getDataService(this.id, this.modulePath);
    },
  },
  created() {
    this.loadData();
  },
};
</script>
