<template>
  <v-form v-model="valid">
    <v-container v-show="!loading" :disabled="loading">
      <v-row v-if="currentMod &&  !!currentMod.overwriteDescription" class="mt-2">
        <td class="ma-2" v-html="currentMod && currentMod.overwriteDescription"></td>
      </v-row>
      <v-row v-else class="mt-2">
        <slot name="header">Slot fehlt</slot>
      </v-row>
      <v-divider class="text-left my-4" />
      <slot name="main">
        Title
      </slot>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        :loading="loading"
        :saving="saving"
        @nextStep="nextStep2"
        @prevStep="prevStep"
        @submit="submit"
        @ignore="ignore"
      />
    </v-container>
    <v-container v-show="loading">
      <Circual/>
    </v-container>
  </v-form>
</template>

<script>
import stepMixin from '@/mixins/stepMixin';
import PrevNextButtons from '@/components/button/PrevNextButton.vue';
import Circual from '@/components/loading/Circual.vue';

export default {
  props: {
    position: {
      type: Number,
    },
    maxPos: {
      type: Number,
    },
    loading: {
      type: Boolean,
      default: true,
    },
    saving: {
      type: Boolean,
      default: false,
    },
    currentMod: {
      type: Object,
    },
  },
  components: {
    PrevNextButtons,
    Circual,
  },
  mixins: [stepMixin],
  methods: {
    nextStep2() {
      this.$emit('nextStep');
    },
  },
  data: () => ({
    valid: true,
  }),
};
</script>
