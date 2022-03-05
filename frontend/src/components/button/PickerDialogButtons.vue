<template>
  <v-card tile>
    <v-card-actions>
      <dialog-buttons @cancel="$emit('cancel')"
                      @ok="$emit('ok')"/>
    </v-card-actions>
  </v-card>
</template>

<script>
import dialogButtons from './dialogButtons.vue';

export default {
  components: {
    dialogButtons,
  },
};
</script>
