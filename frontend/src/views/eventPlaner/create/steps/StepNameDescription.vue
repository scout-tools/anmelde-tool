<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container>
      <v-row>
        <span class="text-left subtitle-1">
          <p>Willkommen bei der <b> Aktionserstellung </b>.</p>
          Viele Pfadfinder_innen und Pfadfinder freuen sich schon auf deine
          Aktion. Im folgenden führen wir dich durch {{ maxPos }} kleine
          Schritte. Viel Spaß!
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
import { required, maxLength, minLength } from 'vuelidate/lib/validators';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import serviceMixin from '@/mixins/serviceMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';

export default {
  name: 'StepNameDescription',
  props: [
    'position',
    'maxPos',
    'event',
  ],
  header: 'Aktionsbeschreibung',
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
        name: 'Name',
        techName: 'name',
        tooltip: 'Wie ist der Lagername?',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Zusammenfassung',
        techName: 'shortDescription',
        tooltip: 'Beschreibe dein Lager in einem Satz.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Beschreibung',
        techName: 'longDescription',
        tooltip: 'Dieser Text wird auf der Startseite angezeigt, wenn jemand auf deine Veranstaltung auswählt.',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'html',
        default: '',
        cols: 12,
      },
    ],
  }),
  validations: {
    data: {
      name: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(35),
      },
      shortDescription: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(100),
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
  // created() {
  //   this.loadData();
  // },
};
</script>
