<template>
  <v-form ref="StepVisibility" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Ist die Veranstaltung schon öffentlich?
          Wenn Nein, wird sie in der Liste nicht angezeigt,
          kann aber natürlich jederzeit bearbeitet werden.
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
  name: 'StepMasterData',
  props: ['position', 'maxPos'],
  header: 'Stammdaten',
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
        name: 'Öffentlich sichtbar?',
        techName: 'isPublic',
        tooltip: '123',
        icon: 'mdi-eye',
        mandatory: true,
        fieldType: 'checkbox',
        default: '',
      },
    ],
  }),
  validations: {
    data: {
      isPublic: {
        required,
      },
    },
  },
  methods: {
    beforeTabShow() {
      this.loadData();
    },
    loadData() {
      this.getService(this.id, this.modulePath);
    },
  },
  created() {
    this.loadData();
  },
};
</script>
