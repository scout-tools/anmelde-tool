<template>
  <v-form v-model="valid">
    <v-container v-if="!isLoadingProp">
      <v-row class="mt-2">
        <slot name="header">Title</slot>
      </v-row>
      <v-divider class="text-left my-2" />
      <slot name="main">Title</slot>
      <v-divider class="my-3" />
      <prev-next-buttons
        :position="position"
        :max-pos="maxPos"
        @nextStep="nextStep"
        @prevStep="prevStep"
        @submit="submit"
        @ignore="ignore"
      />
    </v-container>
    <v-container v-else>
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
    isloading: {
      type: Boolean,
      default: true,
    },
  },
  computed: {
    isLoadingProp() {
      return !!this.isloading;
    },
  },
  components: {
    PrevNextButtons,
    Circual,
  },
  mixins: [stepMixin],
  data: () => ({
    valid: true,
  }),
};
</script>
