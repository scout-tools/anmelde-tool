<template>
<v-container>
  <v-form v-model="valid">
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="normal"
          color="brown"
          label="Normale Teilnehmer_innen"
          min=0
          :max="total"
          thumb-label="always"
          readonly
        >
        </v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="helper"
          color="red"
          label="Helferlein"
          min=0
          :max="maxHelper"
          thumb-label="always"
          type="number"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="stammes"
          color="blue"
          label="Stammesvertretung"
          min=0
          :max="maxStammes"
          thumb-label="always"
          type="number"
        ></v-slider>
      </v-col>
    </v-row>
    <v-row>
      <v-col col=12>
        <v-slider
          v-model="groupLeader"
          color="green"
          label="Gruppenleiter_innen"
          min=0
          :max="maxGroupLeader"
          thumb-label="always"
          type="number"
        ></v-slider>
      </v-col>
    </v-row>
  </v-form>
</v-container>
</template>

<script>
export default {
  data: () => ({
    total: 20,
    helper: 0,
    stammes: 0,
    groupLeader: 0,
    valid: false,
  }),
  computed: {
    normal() {
      return this.total - this.helper - this.stammes - this.groupLeader;
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
