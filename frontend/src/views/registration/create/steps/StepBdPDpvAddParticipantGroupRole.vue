<template>
  <v-form ref="formParticipantGroupRole" v-model="valid">
    <v-container>
      <span class="subtitle-2">
        Du kannst dies Antahl der Teilnehmenden bis zum 1. Mai 2021 anpassen.
        <br />
        Dafür kannst du dich dafür jederzeit wieder einloggen.</span
      >
      <v-form v-model="valid">
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="normal"
              color="orange"
              label="Normale Teilnehmer_innen"
              min="1"
              max="200"
              thumb-label="always"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span> {{tooltip.normal}} </span>
                </v-tooltip>
              </template>
            </v-slider>
          </v-col>
        </v-row>
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="groupLeader"
              color="grey"
              label="Gruppenleiter_innen"
              min="1"
              thumb-label="always"
              type="number"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span> {{tooltip.groupLeader}} </span>
                </v-tooltip>
              </template></v-slider
            >
          </v-col>
        </v-row>
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="stammes"
              color="blue"
              label="Stammesvertretung"
              min="1"
              thumb-label="always"
              type="number"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span> {{tooltip.stammes}} </span>
                </v-tooltip>
              </template></v-slider
            >
          </v-col>
        </v-row>
        <v-row>
          <v-col col="12">
            <v-slider
              v-model="helper"
              color="red"
              label="Helferlein"
              min="0"
              thumb-label="always"
              type="number"
            >
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span> {{tooltip.helper}} </span>
                </v-tooltip>
              </template></v-slider
            >
          </v-col>
        </v-row>
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
              <template slot="append">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon color="success" dark v-bind="attrs" v-on="on">
                      mdi-help-circle-outline
                    </v-icon>
                  </template>
                  <span> {{tooltip.total}} </span>
                </v-tooltip>
              </template></v-slider
            >
          </v-col>
        </v-row>
      </v-form>
      {{
        `Du hast ${total} Personen angemeldet.Das entspricht einem Teilnehmerbeitrag von maximal ${
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
  displayName: 'Teilnehmer_innen Rolle',

  components: {
    // RolePicker,
    PrevNextButtons,
  },
  props: ['position', 'maxPos'],
  data: () => ({
    tooltip: {
      normal: 'Das sind die allgemeinen Gruppenkinder, die aktiv am Spiel teilnehmen',
      helper: 'Auch diese nehmen aktiv am Spiel teil, sollten aber Aufsichtspflichten erfüllen',
      stammes: 'Hier sind lediglich wenige Menschen pro Stamm notwendig (max. 3, eher weniger), sie sind aktive SpielerInnen mit Koordinationsaufgaben',
      groupLeader: 'Alle, die keine Lust haben auf der aktiven Spielseite zu stehen, sondern lieber hinter oder auf der Bühne die Fäden ziehen wollen, können sich hier melden',
      total: 'Many ist eine Tomate',
    },
    displayName: 'Essen',
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
  },
};
</script>

<style scoped>
</style>
