<template>
  <v-form ref="formNameDescription" v-model="valid">
    <v-container class="px-0" fluid>
      <v-container>
        <p>
          Wir würden uns freuen, wenn Du hier noch weitere Heime und/oder
          Lagerplätze einträgst, die sich für das Spiel eignen.
        </p>

        <v-divider class="my-2" />

        <v-btn color="primary" @click="newLocation()">
          Platz oder Haus vorschlagen
        </v-btn>
        <v-list v-if="!isLoading">
          <v-subheader>Orte</v-subheader>
          <v-list-item-group color="primary">
            <v-list-item
              v-for="(item, i) in items"
              :key="i"
            >
              <v-list-item-avatar>
                <v-icon color="black" dark>mdi-home</v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title
                  v-text="item.name + ' - ' + item.description"
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
              v-if="!items.length"
            >
              Bisher hast du noch kein Ort hinzugefügt.
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <div v-else>
          <div class="text-center ma-5">
          <p>
            Lade Daten
          </p>
            <v-progress-circular
              :size="80"
              :width="10"
              color="primary"
              indeterminate
            ></v-progress-circular>
          </div>
        </div>
      </v-container>
      <v-divider class="my-3" />

      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep()"
        @prevStep="prevStep"
        @submitStep="submitStep()"
      />
    </v-container>
    <delete-location-modal
      ref="deleteLocationModal"
      @refresh="onRefresh()"
    />
    <create-location-dialog
      ref="newLocationDialog"
      @close="onCloseWindow()"
      @refresh="onRefresh()"
    />
  </v-form>
</template>

<script>
import axios from 'axios';
import CreateLocationDialog from '@/views/event/create/components/dialog/CreateLocationDialog.vue';
import DeleteLocationModal from '@/views/registration/create/steps/dialog/DeleteLocationModal.vue';
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';

export default {
  name: 'StepBdpDpvLocationSuggention',
  displayName: 'Heim-/Zeltplatzvorschläge',
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
    isLoading: true,
    items: [{ locations: [] }],
  }),
  validations: {},
  watch: {
    radioGroup(value) {
      this.$store.commit('setDpvAddedLocation', value === '1');
    },
  },
  methods: {
    newLocation() {
      this.$refs.newLocationDialog.openDialog();
    },
    onCloseWindow() {
      // this.$store.commit('setDpvAddedLocation', true);
    },
    validate() {
      this.$v.$touch();
      console.log(!this.$v.$error);
      this.valid = !this.$v.$error;
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
    getLocations() {
      this.isLoading = true;
      Promise.all([this.loadRegistrationEventLocations()])
        .then((values) => {
          [this.items] = values;
          this.isLoading = false;
          console.log(this.items);
        })
        .catch((error) => {
          this.errormsg = error.response.data.message;
          this.isLoading = false;
        });
    },
    async loadRegistrationEventLocations() {
      const path = `${this.API_URL}basic/event-location/?registration=${this.$route.params.id}`;
      const response = await axios.get(path);

      return response.data;
    },
    onRefresh() {
      this.getLocations();
    },
    editLocation(id) {
      this.$refs.newLocationDialog.openDialogEdit(
        this.items.filter((i) => i.id === id)[0],
      );
    },
    deleteLocation(item) {
      this.$refs.deleteLocationModal.show(item);
    },
    getData() {
      return {
        name: this.data.name,
        description: this.data.description,
      };
    },
    beforeTabShow() {
      this.onRefresh();
    },
  },
  created() {
    this.$store.commit('setDpvAddedLocation', false);
  },
};
</script>

<style>
</style>
