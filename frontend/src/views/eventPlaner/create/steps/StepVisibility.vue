<template>
  <v-form ref="StepVisibility" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Lege für die Aktion einen 6-Stelligen Verifizierungscode fest. <br/>
          Dieser besteht aus Buchstaben und Zahlen und wird bei der Anmeldung
          mitgeschickt, damit sich die Anmelder verifizieren können, dass sie
          eingeladen wurden. <br/>
          Bei leerem Feld gibt es keinen Verifizierungscode.
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-col cols="3">
          <v-switch label="Sichtbar" v-model="isPublic"></v-switch>
        </v-col>
      </v-row>

      <v-divider class="my-3"/>

      <prev-next-button
        :position="position"
        :max-pos="maxPos"
        :valid="valid"
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
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import store from '@/store';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';

export default {
  name: 'StepVisibility',
  header: 'Sichtbarkeit',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
  },
  mixins: [stepMixin],
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    isPublic: false,
  }),
  computed: {
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    updateData() {
      store.commit('createEvent/setEventAttribute', {
        prop: 'isPublic',
        value: this.isPublic,
      });
    },
  },
  mounted() {
    this.isPublic = this.event.isPublic;
  },
};
</script>
