<template>
  <div>
    <h1 style="margin-top: 80px; margin-left: 40px">PDF generieren</h1>
    <v-btn :disabled="!pdfContentIsReady" @click="generatePdf()"> generate </v-btn>
    <pdf-content-page ref="pdfContentPage" @loadingDone="updatePage()"/>
  </div>
</template>

<script>
import pdfContentPage from '@/views/pdfGeneration/PdfContentPage.vue';
import html2pdf from 'html2pdf.js';

export default {
  name: 'pdfGeneration',
  components: { pdfContentPage },
  data: () => ({
    pdfContentIsReady: false,
    documentCounter: 0,
  }),
  computed: {
    htmlToPdfOptions() {
      const { groupsPerChunk } = this.$refs.pdfContentPage.$data;
      const maxLength = this.$refs.pdfContentPage.$data.allGroups.length;
      const min = this.documentCounter * groupsPerChunk + 1;
      const max = (min + groupsPerChunk > maxLength) ? maxLength : min + groupsPerChunk - 1;

      const filename = `stämme${min}_${max}.pdf`;
      return {
        filename,
        enableLinks: true,
        html2canvas: {
          useCORS: true,
        },
      };
    },
  },
  methods: {
    updatePage() {
      this.pdfContentIsReady = true;
      this.$forceUpdate();
    },
    async generatePdf() {
      await this.$refs.pdfContentPage.setCurrent(this.documentCounter);
      await html2pdf().from(this.$refs.pdfContentPage.$el).set(this.htmlToPdfOptions).save();
      await this.afterDownload();
    },
    async afterDownload() {
      const { groupsPerChunk, allGroups } = this.$refs.pdfContentPage.$data;
      this.documentCounter += 1;
      if (allGroups.length / groupsPerChunk > this.documentCounter) {
        await this.generatePdf(); // generates next pdf document (e.g. recursion)
      } else {
        // resets DOM
        this.documentCounter = 0;
        this.pdfContentIsReady = false;
        await this.$refs.pdfContentPage.setCurrent(this.documentCounter);
      }
    },
  },
};
</script>
