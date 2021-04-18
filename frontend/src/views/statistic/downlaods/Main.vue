<template>
  <v-tabs vertical icons-and-text class="pa-0">
    <v-tab>
      <v-icon left> mdi-microsoft-excel </v-icon>
      Excel
    </v-tab>
    <v-tab class="pa-0">
      <v-icon left> mdi-file-pdf </v-icon>
      PDFs
    </v-tab>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <file-download />
        </v-card-text>
      </v-card>
    </v-tab-item>

    <v-tab-item>
      <v-card flat>
        <v-card-text>
          <pdf-generation-interface />
        </v-card-text>
      </v-card>
    </v-tab-item>
  </v-tabs>
</template>

<script>
import PdfGenerationInterface from './PdfGenerationInterface.vue';
import FileDownload from './FileDownload.vue';

export default {
  components: {
    PdfGenerationInterface,
    FileDownload,
  },
};
</script>
