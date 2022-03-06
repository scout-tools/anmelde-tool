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
        <BaseField :field="field" v-model="data[field.techName]" :valdiationObj="$v" />
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
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import PrevNextButton from '@/components/button/PrevNextButton.vue';
import BaseField from '@/components/common/BaseField.vue';
import store from '@/store';

export default {
  name: 'StepNameDescription',
  props: ['position', 'maxPos'],
  header: 'Aktionsbeschreibung',
  components: {
    PrevNextButton,
    BaseField,
  },
  mixins: [stepMixin, apiCallsMixin],
  data: () => ({
    valid: true,
    data: {},
    fields: [
      {
        name: 'Name',
        techName: 'name',
        tooltip: '123',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Zusammenfassung',
        techName: 'description',
        tooltip: '123',
        icon: 'mdi-account-circle',
        mandatory: true,
        fieldType: 'textfield',
        default: '',
      },
      {
        name: 'Beschreibung',
        techName: 'text',
        tooltip: '123',
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
        maxLength: maxLength(20),

      },
      description: {
        required,
        minLength: minLength(1),
        maxLength: maxLength(100),
      },
    },
  },
  computed: {
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message:
            'Deine eingegeben Daten scheinen nicht gültig zu sein, bitte überprüfe dies noch einmal',
          color: 'error',
        });
      } else {
        store.commit('createEvent/setEventName', this.data.name);
        store.commit('createEvent/setEventDescription', this.data.description);
      }
    },
  },
  mounted() {
    if (this.event.name !== 'Dummy') {
      this.data.name = this.event.name;
    }
    this.data.description = this.event.description;
    this.$forceUpdate();
  },
};
</script>
