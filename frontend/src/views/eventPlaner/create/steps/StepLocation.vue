<template>
  <v-form
    ref="formLocation"
    v-model="valid">
    <v-container>
      <v-row class="mt-6">
        <span class="subtitle-1">
          {{ 'Wähle hier den Veranstaltungsort aus.' }}
        </span>
      </v-row>
      <v-row>
        <v-select
          v-model="selectedLocation"
          :items="items"
          :error-messages="selectedLocationErrors"
          item-text="preview"
          item-value="id"
          label="Veranstaltungsort wählen"
          required
          @input="validate()"
        />
      </v-row>
      <v-row>
        <p class="mr-4">
          Oder erstelle zuerst einen neuen Ort:
        </p>
        <v-btn
          small
          color="secondary"
          @click="newLocation()">
          Neuen Ort anlegen
        </v-btn>
        <create-location-dialog ref="newLocationDialog" @close="getEventLocations()"/>
      </v-row>
      <v-divider class="my-4"/>
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
import CreateLocationDialog from '@/components/dialogs/CreateLocationDialog.vue';
import PrevNextButton from '@/components/buttons/PrevNextButton.vue';
import stepMixin from '@/mixins/stepMixin';
import apiCallsMixin from '@/mixins/apiCallsMixin';
import store from '@/store';

export default {
  name: 'StepLocation',
  header: 'Ort',
  props: ['position', 'maxPos'],
  mixins: [stepMixin, apiCallsMixin],
  components: {
    CreateLocationDialog,
    PrevNextButton,
  },
  data: () => ({
    items: [],
    selectedLocation: null,
    locationDialog: false,
    API_URL: process.env.VUE_APP_API,
    valid: true,
  }),
  validations: {
    selectedLocation: {
      required,
    },
  },
  computed: {
    selectedLocationErrors() {
      const errors = [];
      if (!this.$v.selectedLocation.$dirty) return errors;
      if (!this.$v.selectedLocation.required) {
        errors.push('Es muss ein Veranstaltungsort ausgewählt werden.');
      }
      return errors;
    },
    ...mapGetters({
      event: 'createEvent/event',
    }),
  },
  methods: {
    async getEventLocations() {
      this.getEventLocation()
        .then((success) => {
          this.items = success.data;
          this.formatLocationPreview();
        })
        .catch(() => {
          this.$root.globalSnackbar.show({
            message: 'Leider ist ein Problem beim runterladen der möglichen Locations aufgetreten, bitte probiere es später noch einmal.',
            color: 'error',
          });
        });
    },
    formatLocationPreview() {
      this.items = this.items.map(({
        name,
        description,
        address,
        zipCode,
        ...args
      }) => ({
        preview: `${name}: ${description} (${address}, ${zipCode.zipCode} ${zipCode.city})`,
        ...args,
      }));
    },
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    updateData() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        this.$root.globalSnackbar.show({
          message: 'Deine eingegeben Daten scheinen nicht gültig zu sein, bitte überprüfe dies noch einmal',
          color: 'error',
        });
      } else {
        store.commit('createEvent/setEventAttribute', {
          prop: 'location',
          value: this.selectedLocation,
        });
      }
    },
  },
  mounted() {
    this.getEventLocations();
    this.selectedLocation = this.event.location;
  },
};
</script>
