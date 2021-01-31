<template>
  <v-container>
    <v-form v-model="valid">
      <v-row>
        <v-col col="12">
          <v-slider
            v-model="normal"
            color="orange"
            label="Normale Teilnehmer_innen"
            min="0"
            thumb-label="always"
          >
            <template slot="append">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon color="success" dark v-bind="attrs" v-on="on">
                    mdi-help-circle-outline
                  </v-icon>
                </template>
                <span> Blub </span>
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
                <span> Blub </span>
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
                <span> Blub </span>
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
                <span> Blub </span>
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
                <span> Blub </span>
              </v-tooltip>
            </template></v-slider
          >
        </v-col>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    normal: 0,
    helper: 0,
    stammes: 0,
    groupLeader: 0,
    valid: false,
  }),
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
};
</script>

<style scoped>
</style>
