<template>
  <v-dialog
    v-model="dialog"
    @keydown.esc="cancel"
    max-width="600">
    <v-card>
      <v-card-title class="text-h5 grey lighten-2">
        {{ title }}
      </v-card-title>
      <v-card-text
          class="mt-5"
          v-show="!!message">
        {{ message }}
      </v-card-text>
      <v-card-actions class="pt-3">
        <v-spacer/>
        <v-btn
          v-if="!noconfirm"
          depressed color="secondary" elevation="2"
          @click.native="cancel">
          {{ noText }}
        </v-btn>
        <v-btn
          depressed color="red" elevation="2"
          @click.native="agree">
          {{ yesText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'YesNoDialog',
  data() {
    return {
      dialog: false,
      resolve: null,
      reject: null,
      message: null,
      title: null,
      noconfirm: false,
      yesText: 'Ja',
      noText: 'Nein',
    };
  },

  methods: {
    open(title, message, yesText = 'Ja', noText = null) {
      this.dialog = true;
      this.title = title || 'missing title';
      this.message = message || 'missing message';
      this.yesText = yesText || 'Ja';
      if (noText) {
        this.noconfirm = false;
        this.noText = noText || 'Nein';
      } else {
        this.noconfirm = true;
        this.noText = '';
      }
      return new Promise((resolve, reject) => {
        this.resolve = resolve;
        this.reject = reject;
      });
    },
    agree() {
      this.resolve(true);
      this.dialog = false;
    },
    cancel() {
      this.resolve(false);
      this.dialog = false;
    },
  },
};
</script>
