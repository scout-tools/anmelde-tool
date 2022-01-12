<template>
  <v-form ref="StepEventModul" v-model="valid">
    <v-container>
      <v-row class="mb-6">
        <span class="subtitle-1">
          Lege für die Aktion Tags fest. <br/>
          Mit den Tags können die Aktionen besser sortiert und gefiltert werden,
          was die Benutzerfreundlichkeit erhöht.
          <br/> Es gibt eine Vorauswahl an Tags, du kannst aber auch eigne hinzufügen.
        </span>
      </v-row>
      <v-row align="center" justify="center">
        <v-select
          v-model="eventTags"
          :items="eventTagList"
          :error-messages="eventTagsErrors"
          item-text="name"
          item-value="id"
          label="Event Tags wählen"
          multiple
          required
          @input="validate"
        />
      </v-row>

      <v-row class="mt-6">
        <span class="subtitle-1">
          Für welche Zielgruppe(n) ist deine Aktion?
        </span>
      </v-row>
      <v-row>
        <v-select
          v-model="ageGroups"
          :items="ageGroupList"
          :error-messages="ageGroupsErrors"
          item-text="name"
          item-value="id"
          label="Zielgruppe(n) wählen"
          multiple
          required
          @input="validate"/>
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
import { required } from 'vuelidate/lib/validators';
import { mapGetters } from 'vuex';
import stepMixin from '@/mixins/stepMixin';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import store from '@/store';

export default {
  name: 'StepEventTags',
  header: 'Tags',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButton,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    eventTagList: [],
    eventTags: [],
    ageGroupList: [],
    ageGroups: [],
  }),
  mixins: [stepMixin, apiCallsMixin],
  validations: {
    eventTags: {
      required,
    },
    ageGroups: {
      required,
    },
  },
  computed: {
    eventTagsErrors() {
      const errors = [];
      if (!this.$v.eventTags.$dirty) return errors;
      if (!this.$v.eventTags.required) {
        errors.push('Nötig');
      }
      return errors;
    },
    ageGroupsErrors() {
      const errors = [];
      if (!this.$v.ageGroups.$dirty) return errors;
      if (!this.$v.ageGroups.required) {
        errors.push('Es muss mindestens eine Zielgruppe ausgewählt werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    async getEventTags() {
      this.getTag('event-tag')
        .then((success) => {
          this.eventTagList = success.data;
          const eventTagIds = this.eventTagList.map((obj) => obj.id);
          this.eventTags = this.event.tags.filter((element) => eventTagIds.includes(element));
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim runterladen der möglichen Event Tags aufgetreten,'
              + ' bitte probiere es später noch einmal.',
            color: 'error',
          });
        });
    },
    async getAvailableAgeGroups() {
      this.getTag('age-group')
        .then((success) => {
          this.ageGroupList = success.data;
          const ageTagIds = this.ageGroupList.map((obj) => obj.id);
          this.ageGroups = this.event.tags.filter((element) => ageTagIds.includes(element));
        })
        .catch((error) => {
          console.log(error);
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim runterladen der Daten aufgetreten,'
              + ' bitte probiere es später noch einmal.',
            color: 'error',
          });
        });
    },
    updateData() {
      store.commit(
        'createEvent/setEventTags',
        [...new Set([...this.ageGroups, ...this.eventTags])],
      );
    },
  },
  mounted() {
    this.getEventTags();
    this.getAvailableAgeGroups();
  },
};
</script>
