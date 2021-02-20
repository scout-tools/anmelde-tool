<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-expand-transition>
        <v-container>
          <span>
            <b
              >Das Heim/Der Zeltplatz meines Stammes kann für die Aktion genutzt
              werden.
            </b>
            <br />
            <br />
            Notwendig sind:
            <ul>
              <li>Möglichkeiten zum Kochen (Herd/Feuerstelle)</li>
              <li>ausreichend Toiletten und fließend Wasser</li>
            </ul>
          </span>
          <v-radio-group v-model="radioGroup">
            <v-radio label="Ja" value="1"></v-radio>
            <v-radio :disabled="!!location.length" label="Nein" value="2"></v-radio>
          </v-radio-group>
        </v-container>
      </v-expand-transition>

      <v-expand-transition>
        <v-container v-show="radioGroup === '1'">
          <v-btn
            color="primary"
            @click="newLocation()"
          >
            Platz oder Haus Hinzufügen
          </v-btn>
      <v-list-item-group color="primary">
        <v-container>
        <v-list-item
          v-for="(item, i) in location"
          :key="i"
        >
          <v-list-item-avatar>
            <v-icon color="black" dark>mdi-home</v-icon>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              v-text="item.name"
            ></v-list-item-title>
          </v-list-item-content>
          <v-list-item-action>
            <v-btn dense icon @click="editLocation(item.id)">
              <v-icon color="primary lighten-1">mdi-pencil</v-icon>
            </v-btn>
          </v-list-item-action>
          <v-list-item-action>
            <v-btn dense icon @click="deleteLocation(item.id)">
              <v-icon color="red lighten-1">mdi-trash-can</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-list-item
          v-if="!location.length"
        >
          Bisher hast du noch niemanden hinzugefügt.
        </v-list-item>
        </v-container>
      </v-list-item-group>
        </v-container>
      </v-expand-transition>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <create-location-dialog
      ref="newLocationDialog"
      @close="onCloseWindow()"
      @refresh="onRefresh()"
    />
    <delete-location-modal ref="deleteLocationModal" @refresh="onRefresh()" />
  </v-form>
</template>

<script>
import axios from 'axios';
import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import DeleteLocationModal from '@/views/registration/create/steps/dialog/DeleteLocationModal.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocation',
  displayName: 'Unser Heim/Zeltplatz',
  props: ['position', 'maxPos'],
  components: {
    PrevNextButtons,
    CreateLocationDialog,
    DeleteLocationModal,
  },
  data: () => ({
    API_URL: process.env.VUE_APP_API,
    valid: true,
    radioGroup: 0,
    radioGroup2: 0,
    value: '0',
    event_location_types: [
      { state: 'Zeltplatz', abbr: 1 },
      { state: 'Heim', abbr: 2 },
    ],
    show_event_location_types: [1, 2],
    addOwnLocation: 0,
    location: [],
    isLoading: true,
  }),
  validations: {},
  watch: {
    location(value) {
      this.$store.commit('setDpvAddedLocation', !!value.length);
    },
  },
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.event_location_types = this.event_location_types;
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      // this.$store.commit('setDpvAddedLocation', true);
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
      this.valid = !this.$v.$error;

      this.valid = this.radioGroup === '2' || this.location.length;
    },
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('nextStep');
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    getLocation() {
      this.isLoading = true;
      Promise.all([this.loadRegistrationEventLocations()])
        .then((values) => {
          [this.location] = values;
          this.isLoading = false;
          this.location = this.location.filter((item) =>
            this.show_event_location_types.includes(item.locationType), // eslint-disable-line
          ); // eslint-disable-line
          console.log(this.location);
        })
        .catch((error) => {
          console.log(error);
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadRegistrationEventLocations() {
      const path = `${this.API_URL}basic/event-location/?registration=${this.$route.params.id}`;
      const response = await axios.get(path);
      return response.data;
    },
    editLocation(id) {
      this.$refs.newLocationDialog.event_location_types = this.event_location_types;
      this.$refs.newLocationDialog.openDialogEdit(
        this.location.filter((i) => i.id === id)[0],
      );
    },
    deleteLocation(item) {
      this.$refs.deleteLocationModal.show(item);
    },
    beforeTabShow() {
      this.onRefresh();
    },
    onRefresh() {
      this.getLocation();
    },
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
