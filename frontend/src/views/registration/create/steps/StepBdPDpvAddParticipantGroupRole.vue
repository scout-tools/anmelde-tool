<template>
  <v-form ref="formParticipantGroupRole" v-model="valid">
    <v-container>
      <p>
        Du kannst die Anzahl der Teilnehmenden bis zum 01.Mai 2021 anpassen.
        <br />
        <br />
        Dafür kannst du dich jederzeit wieder einloggen. <br />
        <br />
        Diese Anmeldung bezieht sich auf das gesamte Wochenende. Personen, die
        früher fahren oder später kommen zählen als vollwertige teilnehmende
        Person.
      </p>
      <v-form v-model="valid">
        <v-divider class="py-3 mt-5" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="normal"
              color="orange"
              label="Teilnehmende"
              min="1"
              max="200"
              thumb-label="always"
            >
            </v-slider>
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.normal }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="groupLeader"
              color="grey"
              label="Gruppenleitung"
              min="0"
              max="30"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.groupLeader }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="stammes"
              color="blue"
              label="Stammesvertretung"
              min="1"
              max="3"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.stammes }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="helper"
              color="red"
              label="Helferlein"
              min="0"
              max="50"
              thumb-label="always"
              type="number"
            />
            <v-row class="ml-5">
              <p>
                <v-icon color="success" dark> mdi-help-circle-outline </v-icon>
                {{ tooltip.helper }}
              </p>
            </v-row>
          </v-col>
        </v-row>
        <v-divider class="py-4 ma-0" />
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="total"
              color="green"
              label="Gesamt"
              thumb-label="always"
              max="200"
              type="number"
              readonly
            >
            </v-slider>
          </v-col>
        </v-row>
      </v-form>
      <v-divider class="py-4 ma-0" />
      {{
        `Du hast ${total} Personen angemeldet. Das entspricht einem Stammesbeitrag von maximal ${
          total * 10
        } €`
      }}
    </v-container>
    <v-divider class="my-3" />

    <prev-next-buttons
      :position="position"
      :max-pos="maxPos"
      @nextStep="nextStep()"
      @prevStep="prevStep"
      @submitStep="submitStep()"
    />
  </v-form>
</template>

<script>
import PrevNextButtons from '../components/button/PrevNextButtonsSteps.vue';
// import RolePicker from '../components/RolePicker..vue';

export default {
  name: 'StepAddParticipantGroupRole',
  displayName: 'Teilnehmende',

  components: {
    // RolePicker,
    PrevNextButtons,
  },
  props: ['position', 'maxPos'],
  data: () => ({
    tooltip: {
      normal:
        'Das sind die Kinder/Jugendliche in den Gruppen, die aktiv am Spiel teilnehmen.',
      groupLeader:
        'Auch diese nehmen aktiv am Spiel teil und haben die Aufsichtspflicht.',
      stammes:
        'Hier sind lediglich wenige Menschen pro Stamm notwendig (max. 3, eher weniger), auch sie nehmen aktiv am Spiel teil und haben Koordinationsaufgaben.',
      helper:
        'Alle, die keine Lust haben auf der aktiven Spielseite zu stehen, sondern lieber hinter oder auf der Bühne die Fäden ziehen wollen, können sich hier melden.',
      total: 'Many ist eine Tomate',
    },
    displayName: 'Essgewohnheiten',
    normal: 0,
    helper: 0,
    stammes: 0,
    groupLeader: 0,
    valid: false,
  }),
  validations: {},
  computed: {
    total() {
      return this.normal + this.helper + this.stammes + this.groupLeader;
    },
    maxHelper() {
      return this.total - this.stammes - this.groupLeader;
    },
    maxStammes() {
      return this.total - this.helper - this.groupLeader;
    },
    maxGroupLeader() {
      return this.total - this.helper - this.stammes;
    },
  },
  methods: {
    validate() {},
    prevStep() {
      this.$emit('prevStep');
    },
    nextStep() {
      this.validate();
      if (!this.valid) {
        return;
      }

      this.addMeatEaters();
    },
    submitStep() {
      this.validate();
      if (!this.valid) {
        return;
      }
      this.$emit('submit');
    },
    addMeatEaters() {
      this.$emit('nextStep');
    },
    beforeTabShow() {},
  },
};
</script>

<style scoped>
</style>
